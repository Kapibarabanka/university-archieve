using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SP
{
    public static class AssemblerHelper
    {
	    public static string Prologue =
			@".586
.model flat, stdcall

include D:\masm32\include\msvcrt.inc
include D:\masm32\include\kernel32.inc
include D:\masm32\include\user32.inc

includelib D:\masm32\lib\msvcrt.lib
includelib D:\masm32\lib\kernel32.lib
includelib D:\masm32\lib\user32.lib

.data
	int_fmt db "" % d"",10, 0
	flt_fmt db "" % f"",10, 0
	buff dq 0
	int_buf dd 0
";

		public static string Main =
@".code

main:

";

		public static string Epilogue =
			@"

	invoke ExitProcess, 0
end main";

        public static Dictionary<VariableType, int> SizesInBytes = new Dictionary<VariableType, int>
        {
            {VariableType.Char,  1},
            {VariableType.SignedChar,  1},
            {VariableType.UnsignedChar,  1},

            {VariableType.Short,  2},
            {VariableType.UnsignedShort,  2},

            {VariableType.Int,  4},
            {VariableType.UnsignedInt,  4},

            {VariableType.Long,  4},
            {VariableType.UnsignedLong,  4},

            {VariableType.LongLong,  8},
            {VariableType.UnsignedLongLong,  8},

            {VariableType.Float,  4},
            {VariableType.Double,  4},

            {VariableType.Pointer,  8},

            {VariableType.Error,  0},
        };

        public static Dictionary<VariableType, string> SizesInAssembler = new Dictionary<VariableType, string>
        {
	        {VariableType.Char,  "db"},
	        {VariableType.SignedChar,  "db"},
	        {VariableType.UnsignedChar,  "db"},

	        {VariableType.Short,  "dw"},
	        {VariableType.UnsignedShort,  "dw"},

	        {VariableType.Int,  "dd"},
	        {VariableType.UnsignedInt,  "dd"},

	        {VariableType.Long,  "dd"},
	        {VariableType.UnsignedLong,  "dd"},

	        {VariableType.LongLong,  "dq"},
	        {VariableType.UnsignedLongLong,  "dq"},

	        {VariableType.Float,  "dd"},
	        {VariableType.Double,  "dd"},

	        {VariableType.Pointer,  "dq"},

	        {VariableType.Error,  ""},
        };

        public static List<string> Registers_1b_1 = new List<string>{"al", "bl", "cl", "dl"};
        public static List<string> Registers_1b_2 = new List<string> { "ah", "bh", "ch", "dh" };
        public static List<string> Registers_2b = new List<string> { "ax", "bx", "cx", "dx" };
        public static List<string> Registers_4b = new List<string> { "eax", "ebx", "ecx", "edx" };

        public static Dictionary<string, List<string>> Registers = new Dictionary<string, List<string>>
        {
	        {"db", Registers_1b_1 },
	        {"dw", Registers_2b },
	        {"dd", Registers_4b },
		};
	}
}
