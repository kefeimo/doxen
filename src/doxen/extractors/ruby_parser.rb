#!/usr/bin/env ruby
# Ruby API parser using Ripper
# Usage: ruby ruby_parser.rb <ruby_file_path>

require 'ripper'
require 'json'

class RubyAPIParser
  def initialize(file_path)
    @file_path = file_path
    @content = File.read(file_path)
    @sexp = Ripper.sexp(@content)
  end

  def parse
    return { error: "Failed to parse Ruby file" } unless @sexp

    {
      classes: extract_classes(@sexp),
      modules: extract_modules(@sexp),
      methods: extract_top_level_methods(@sexp),
      constants: extract_constants(@sexp),
    }
  end

  private

  def extract_classes(node, namespace = [])
    classes = []
    return classes unless node.is_a?(Array)

    node.each do |child|
      next unless child.is_a?(Array)

      case child[0]
      when :class
        # [:class, [:const_ref, [:@const, "ClassName", [line, col]]], superclass, [:bodystmt, body, ...]]
        class_name = extract_name(child[1])
        superclass = extract_name(child[2])
        line = extract_line(child[1])

        body = child[3]
        methods = extract_methods(body)
        class_constants = extract_constants(body)

        classes << {
          name: class_name,
          superclass: superclass,
          line: line,
          methods: methods,
          constants: class_constants,
          namespace: namespace.join('::'),
        }

        # Recursively check for nested classes
        classes += extract_classes(body, namespace + [class_name])

      else
        # Recursively check children
        classes += extract_classes(child, namespace)
      end
    end

    classes
  end

  def extract_modules(node, namespace = [])
    modules = []
    return modules unless node.is_a?(Array)

    node.each do |child|
      next unless child.is_a?(Array)

      case child[0]
      when :module
        # [:module, [:const_ref, [:@const, "ModuleName", [line, col]]], [:bodystmt, body, ...]]
        module_name = extract_name(child[1])
        line = extract_line(child[1])

        body = child[2]
        methods = extract_methods(body)

        modules << {
          name: module_name,
          line: line,
          methods: methods,
          namespace: namespace.join('::'),
        }

        # Recursively check for nested modules
        modules += extract_modules(body, namespace + [module_name])

      else
        # Recursively check children
        modules += extract_modules(child, namespace)
      end
    end

    modules
  end

  def extract_methods(node)
    methods = []
    return methods unless node.is_a?(Array)

    node.each do |child|
      next unless child.is_a?(Array)

      case child[0]
      when :def
        # [:def, [:@ident, "method_name", [line, col]], [:paren, [:params, ...]], [:bodystmt, ...]]
        method_name = child[1][1]
        line = child[1][2][0]
        params = extract_params(child[2])

        methods << {
          name: method_name,
          line: line,
          parameters: params,
          visibility: 'public',  # Default, will be overridden if needed
        }

      when :defs
        # Class method: [:defs, target, [:@period, ".", ...], [:@ident, "method_name", ...], [:paren, [:params, ...]], ...]
        method_name = child[3][1]
        line = child[3][2][0]
        params = extract_params(child[4])

        methods << {
          name: "self.#{method_name}",
          line: line,
          parameters: params,
          visibility: 'public',
          class_method: true,
        }

      when :command
        # Method visibility modifiers: private, protected, public
        if child[1] && child[1].is_a?(Array) && child[1][0] == :@ident
          visibility = child[1][1]
          if ['private', 'protected', 'public'].include?(visibility)
            # Mark subsequent methods with this visibility
            # (simplified - real implementation would track visibility state)
          end
        end

      else
        # Recursively check children
        methods += extract_methods(child)
      end
    end

    methods
  end

  def extract_top_level_methods(node)
    # Extract only top-level methods (not inside classes/modules)
    methods = []
    return methods unless node.is_a?(Array) && node[0] == :program

    body = node[1]
    return methods unless body.is_a?(Array)

    body.each do |child|
      next unless child.is_a?(Array)

      case child[0]
      when :def
        method_name = child[1][1]
        line = child[1][2][0]
        params = extract_params(child[2])

        methods << {
          name: method_name,
          line: line,
          parameters: params,
        }
      end
    end

    methods
  end

  def extract_params(params_node)
    params = []
    return params unless params_node.is_a?(Array)

    # Find the params array
    params_array = find_params_array(params_node)
    return params unless params_array

    params_array.each do |param|
      next unless param.is_a?(Array)

      case param[0]
      when :@ident
        # Regular parameter
        params << {
          name: param[1],
          type: 'required',
          default: nil,
        }

      when :opt_param, :optblock
        # Optional parameter with default
        param_name = param[1] && param[1][1]
        params << {
          name: param_name,
          type: 'optional',
          default: 'provided',
        }

      when :kwarg
        # Keyword argument: [:kwarg, [:@ident, "name", ...]]
        param_name = param[1] && param[1][1]
        params << {
          name: param_name,
          type: 'keyword',
          default: nil,
        }

      when :kwrest_param
        # **kwargs
        param_name = param[1] && param[1][1]
        params << {
          name: param_name || 'kwargs',
          type: 'keyword_rest',
          default: nil,
        }

      when :rest_param
        # *args
        param_name = param[1] && param[1][1]
        params << {
          name: param_name || 'args',
          type: 'rest',
          default: nil,
        }

      when :blockarg
        # &block
        param_name = param[1] && param[1][1]
        params << {
          name: param_name || 'block',
          type: 'block',
          default: nil,
        }
      end
    end

    params
  end

  def find_params_array(node)
    return nil unless node.is_a?(Array)

    # Look for [:params, ...] or [:paren, [:params, ...]]
    if node[0] == :params
      return node[1..-1]
    elsif node[0] == :paren && node[1].is_a?(Array) && node[1][0] == :params
      return node[1][1..-1]
    end

    # Search children
    node.each do |child|
      result = find_params_array(child)
      return result if result
    end

    nil
  end

  def extract_constants(node)
    constants = []
    return constants unless node.is_a?(Array)

    node.each do |child|
      next unless child.is_a?(Array)

      case child[0]
      when :assign
        # [:assign, [:var_field, [:@const, "CONSTANT_NAME", [line, col]]], value]
        if child[1] && child[1].is_a?(Array) && child[1][0] == :var_field
          var = child[1][1]
          if var && var.is_a?(Array) && var[0] == :@const
            const_name = var[1]
            line = var[2][0]
            value = extract_value(child[2])

            constants << {
              name: const_name,
              line: line,
              value: value,
            }
          end
        end

      else
        # Recursively check children
        constants += extract_constants(child)
      end
    end

    constants
  end

  def extract_name(node)
    return nil unless node.is_a?(Array)

    case node[0]
    when :const_ref
      # [:const_ref, [:@const, "ClassName", [line, col]]]
      node[1] && node[1][1]

    when :const_path_ref
      # Namespaced constant: Module::Class
      parts = []
      collect_const_path(node, parts)
      parts.join('::')

    when :var_ref
      # Variable reference
      node[1] && node[1][1]

    else
      nil
    end
  end

  def collect_const_path(node, parts)
    return unless node.is_a?(Array)

    case node[0]
    when :const_path_ref
      collect_const_path(node[1], parts)
      parts << node[2][1] if node[2]

    when :const_ref, :var_ref
      parts << (node[1] && node[1][1])

    when :top_const_ref
      parts << (node[1] && node[1][1])
    end
  end

  def extract_line(node)
    return nil unless node.is_a?(Array)

    # Traverse to find line number
    node.each do |child|
      if child.is_a?(Array) && child[2].is_a?(Array) && child[2][0].is_a?(Integer)
        return child[2][0]
      end
      result = extract_line(child)
      return result if result
    end

    nil
  end

  def extract_value(node)
    return nil unless node.is_a?(Array)

    case node[0]
    when :@int
      node[1].to_i
    when :@float
      node[1].to_f
    when :string_literal
      # Extract string content
      extract_string(node)
    when :symbol_literal
      # :symbol
      ":#{extract_symbol(node)}"
    when :array
      # [...]
      '[]'
    when :hash
      # {...}
      '{}'
    else
      '<complex>'
    end
  end

  def extract_string(node)
    return nil unless node.is_a?(Array) && node[0] == :string_literal

    content = node[1]
    return nil unless content.is_a?(Array)

    strings = content.select { |n| n.is_a?(Array) && n[0] == :@tstring_content }
    strings.map { |s| s[1] }.join
  end

  def extract_symbol(node)
    return nil unless node.is_a?(Array) && node[0] == :symbol_literal

    content = node[1]
    return nil unless content.is_a?(Array)

    if content[0] == :symbol && content[1].is_a?(Array) && content[1][0] == :@ident
      content[1][1]
    end
  end
end

# Main execution
if ARGV.length != 1
  puts JSON.generate({ error: "Usage: ruby ruby_parser.rb <file_path>" })
  exit 1
end

file_path = ARGV[0]

unless File.exist?(file_path)
  puts JSON.generate({ error: "File not found: #{file_path}" })
  exit 1
end

begin
  parser = RubyAPIParser.new(file_path)
  result = parser.parse
  puts JSON.generate(result)
rescue => e
  puts JSON.generate({ error: e.message, backtrace: e.backtrace[0..5] })
  exit 1
end
