#!/usr/bin/env ruby
# Ruby API parser using YARD (Yet Another Ruby Documentation)
# Usage: ruby ruby_parser_yard.rb <ruby_file_path>

require 'yard'
require 'json'

class RubyYARDParser
  def initialize(file_path)
    @file_path = file_path
    # Use the global YARD registry and clear it
    YARD::Registry.clear
  end

  def parse
    begin
      # Parse the file with YARD (uses global registry)
      YARD.parse(@file_path)

      {
        classes: extract_classes,
        modules: extract_modules,
        methods: extract_top_level_methods,
        constants: extract_constants,
      }
    rescue => e
      {
        error: "Failed to parse with YARD: #{e.message}",
        classes: [],
        modules: [],
        methods: [],
        constants: [],
      }
    end
  end

  private

  def extract_classes
    classes = []

    YARD::Registry.all(:class).each do |yard_class|
      # Skip classes not in this file
      next unless yard_class.file == @file_path

      classes << {
        name: yard_class.name.to_s,
        superclass: yard_class.superclass ? yard_class.superclass.name.to_s : nil,
        line: yard_class.line,
        docstring: extract_docstring(yard_class),
        methods: extract_methods(yard_class),
        attributes: extract_attributes(yard_class),
        namespace: yard_class.namespace.to_s == '' ? nil : yard_class.namespace.to_s,
      }
    end

    classes
  end

  def extract_modules
    modules = []

    YARD::Registry.all(:module).each do |yard_module|
      # Skip modules not in this file
      next unless yard_module.file == @file_path

      modules << {
        name: yard_module.name.to_s,
        line: yard_module.line,
        docstring: extract_docstring(yard_module),
        methods: extract_methods(yard_module),
        namespace: yard_module.namespace.to_s == '' ? nil : yard_module.namespace.to_s,
      }
    end

    modules
  end

  def extract_methods(parent)
    methods = []

    parent.meths.each do |yard_method|
      # Extract parameter information
      params = yard_method.parameters.map do |param_name, default_value|
        # Find @param tag for this parameter
        param_tag = yard_method.tags(:param).find { |t| t.name == param_name.to_s.gsub(/[*&:]/, '') }

        {
          name: param_name.to_s,
          type: param_tag ? param_tag.types&.join(', ') : nil,
          description: param_tag ? param_tag.text : nil,
          default: default_value,
        }
      end

      # Extract return type
      return_tag = yard_method.tag(:return)
      return_type = return_tag ? return_tag.types&.join(', ') : nil
      return_description = return_tag ? return_tag.text : nil

      # Extract examples
      examples = yard_method.tags(:example).map { |ex| ex.text }

      # Extract raise/exception info
      raises = yard_method.tags(:raise).map do |raise_tag|
        {
          type: raise_tag.types&.first,
          description: raise_tag.text,
        }
      end

      methods << {
        name: yard_method.name.to_s,
        line: yard_method.line,
        docstring: extract_docstring(yard_method),
        parameters: params,
        return_type: return_type,
        return_description: return_description,
        visibility: yard_method.visibility.to_s,
        scope: yard_method.scope.to_s, # :instance or :class
        examples: examples,
        raises: raises,
      }
    end

    methods
  end

  def extract_top_level_methods
    methods = []

    YARD::Registry.all(:method).each do |yard_method|
      # Only get methods at root namespace
      next unless yard_method.namespace.to_s == ''
      next unless yard_method.file == @file_path

      # Extract parameter information
      params = yard_method.parameters.map do |param_name, default_value|
        param_tag = yard_method.tags(:param).find { |t| t.name == param_name.to_s.gsub(/[*&:]/, '') }

        {
          name: param_name.to_s,
          type: param_tag ? param_tag.types&.join(', ') : nil,
          description: param_tag ? param_tag.text : nil,
          default: default_value,
        }
      end

      return_tag = yard_method.tag(:return)
      return_type = return_tag ? return_tag.types&.join(', ') : nil

      methods << {
        name: yard_method.name.to_s,
        line: yard_method.line,
        docstring: extract_docstring(yard_method),
        parameters: params,
        return_type: return_type,
      }
    end

    methods
  end

  def extract_attributes(parent)
    attributes = []

    parent.attributes.each do |scope, attr_hash|
      attr_hash.each do |name, attr|
        # attr is a Hash with :read and :write methods
        read_method = attr[:read]
        write_method = attr[:write]

        if read_method
          attributes << {
            name: name.to_s,
            type: extract_attribute_type(read_method),
            line: read_method.line,
            readable: true,
            writable: write_method != nil,
          }
        end
      end
    end

    attributes
  end

  def extract_attribute_type(method)
    return_tag = method.tag(:return)
    return_tag ? return_tag.types&.join(', ') : nil
  end

  def extract_constants
    constants = []

    YARD::Registry.all(:constant).each do |yard_const|
      next unless yard_const.file == @file_path

      constants << {
        name: yard_const.name.to_s,
        line: yard_const.line,
        value: yard_const.value,
        docstring: extract_docstring(yard_const),
      }
    end

    constants
  end

  def extract_docstring(yard_object)
    docstring = yard_object.docstring
    return nil if docstring.nil? || docstring.empty?

    # Return the main docstring text (without tags)
    docstring.to_s.strip
  end
end

# Main execution
if ARGV.length != 1
  puts JSON.generate({ error: "Usage: ruby ruby_parser_yard.rb <file_path>" })
  exit 1
end

file_path = ARGV[0]

unless File.exist?(file_path)
  puts JSON.generate({ error: "File not found: #{file_path}" })
  exit 1
end

begin
  parser = RubyYARDParser.new(file_path)
  result = parser.parse
  puts JSON.generate(result)
rescue => e
  puts JSON.generate({ error: e.message, backtrace: e.backtrace[0..5] })
  exit 1
end
