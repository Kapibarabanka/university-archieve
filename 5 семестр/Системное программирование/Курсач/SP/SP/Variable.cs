using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SP
{
    public enum VariableType
    {
	    Array,

		Bool,
        Char,
        UnsignedChar,
        SignedChar, 
        Short, //short int, signed short int, signed short  
        UnsignedShort, //unsigned short int
        Int, //signed int, signed
        UnsignedInt, //unsigned
		Long, //long int, signed long int, signed long
        UnsignedLong, //unsigned long int
        LongLong, //long long int, signed long long int, signed long long
        UnsignedLongLong, //unsigned long long int
		Float,
        Double,
        Function,
        Void,

        Pointer,

        Error,
    }

    public interface IVariable
    {
	    string Name { get; }
	    VariableType Type { get; }
        int Reg { get; }
    }

    public class Variable : IVariable
    {
        public string Name { get; }
        public VariableType Type { get; }
        public int Reg { get; set; }
        public object Value { get; set; }
        public bool IsTemp = false;
        public bool IsFloat => Type > VariableType.LongLong || Reg > 5;
        public Variable(string name, VariableType type, int reg, object value = null)
        {
            Name = name == "" || name.Contains("[") ? name : "var_"+name;
            Type = type;
            Reg = name == "" || name.Contains("[") ? reg : -1;
            Value = value ?? GetDefaultValue(type);
            if (name == "" || reg != -1) IsTemp = true;
			if(name.Contains("[") )IsTemp = false;
        }

        public override string ToString()
        {
	        return $"{Name} (reg: {Reg}): {Value}";
        }

        public static object GetDefaultValue(VariableType type)
        {
            switch (type)
            {
                case VariableType.Function: return null;
				default: return 0;
            }
        }
    }

    public class Array : IVariable
    {
	    public string Name { get; }
	    public VariableType Type { get; }
        public int Reg { get; }

        public List<Variable> Value { get; set; }
		public int Length { get; }

	    public Array(string name, VariableType type, int length, List<Variable> value = null)
	    {
		    Name = name == "" ? name : "arr_" + name;
		    Type = VariableType.Array;
            Reg = -1;
		    Length = length;
		    if (value != null)
		    {
			    Value = value;
		    }
		    else
		    {
			    Value = new List<Variable>();
			    for (var i = 0; i < length; i++)
                {
	                var size = AssemblerHelper.SizesInBytes[type];
	                var memberName = $"dword ptr[{Name} + {i * size}]";
                    Value.Add(new Variable(memberName, type, -1));
			    }
		    }
	    }

	    public Variable GetAtIndex(int index) => Value[index];

	    public override string ToString()
	    {
		    var result = $"{Name} (reg: {Reg}): [";
		    if (Value is List<Variable> array)
		    {
			    foreach (var variable in array)
			    {
				    result += $" {variable.Value}";
			    }
		    }

		    return result + " ]";
	    }

	}

    public class Pointer : IVariable
    {
	    public string Name { get; }
	    public VariableType Type { get; }
        public int Reg { get; }
        public object Value { get; }

        public string Address { get; }

        public Pointer(string name, VariableType type, int reg, object value = null, string address = null)
        {
			Name = name == "" ? name : "ptr_" + name;
			Type = type;
            Reg = reg;
            Value = value ?? Variable.GetDefaultValue(type);
            Address = address;
        }

        public override string ToString()
        {
            return $"*{Name} (reg: {Reg}): {Value}";
        }
    }
}
