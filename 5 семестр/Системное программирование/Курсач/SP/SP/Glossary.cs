using System;
using System.Collections.Generic;
using System.Linq;

namespace SP
{
	public class Glossary
    {
        public List<string> OtherReservedWords { get; } = new List<string>
        {
            "auto", "break", "case", "const", "continue", "default", "enum", "extern", "goto",
            "inline", "register", "restrict", "return",
            "sizeof", "static", "struct", "switch", "typedef", "union",
            "volatile"
        };

        public List<string> Types { get; } = new List<string>
		{
			"char", "double", "float", "int", "long", "short",
			"void", "signed", "unsigned"
        };

		public List<string> Conditions { get; } = new List<string>
		{
			"if", "else"
		};

		public List<string> Cycles { get; } = new List<string>()
		{
			"while", "for", "do"
		};

        public List<string> OpeningBrackets { get; } = new List<string> { "(", "{", "[" };
	    public List<string> ClosingBrackets { get; } = new List<string> { ")", "}", "]" };
        public List<string> Quotes { get; } = new List<string> { "\"", "'" };

        public List<string> BinaryOperatorsByPriority { get; } = new List<string>
        {
            "[", "(", "->", ".", "*", "/", "%", "+", "-", "<<", ">>", "<", "<=", ">", ">=", "==", "!=", "&", "^", "|", "&&", "||",
            "?", ":", "=", "+=", "-=", "*=", "/=", "%=", "<<=", ">>=", "&=", "^=", "|=", ","
        };

        public static List<string> MathOperators { get; } = new List<string>
        {
	        ".", "*", "/", "%", "+", "-", "<<", ">>", "<", "<=", ">", ">=", "==", "!=", "&", "^", "|", "&&", "||"
        };

		public List<string> AssignationOperators { get; } = new List<string>
        {
            "=", "+=", "-=", "*=", "/=", "%=", "<<=", ">>=", "&=", "^=", "|="
        };
        
		public List<string> IncDecOperators { get; } = new List<string>
		{
			"--", "++"
		};

		public List<string> UnaryBinary { get; } = new List<string>
		{
			"-","+", "*","&"
		};

        public List<string> Punctuation { get; } = new List<string>
        {
            ";", "...", ":", "?"
        };

        public List<string> Pointers { get; } = new List<string>
        {
            "*", "&"
        };

        public List<string> BeforeActionMarkers { get; } = new List<string> { "for", "if", "else", "while", "do", ";" };

		public List<string> Brackets { get; }

        public List<string> ReservedWords { get; }

        public List<string> UnaryOperators { get; }

        public List<string> Operators { get; }

        public List<string> ConsiderAsUnary { get; }

        public Dictionary<TokenType, List<string>> LexemesOfTokenType { get; }

        public Glossary()
        {
            ReservedWords = OtherReservedWords.Union(Types)
                .Union(Conditions).Union(Cycles).ToList();
            UnaryOperators = IncDecOperators.Union(UnaryBinary).Union(new List<string> { "!", "~" }).ToList();
            Operators =
                BinaryOperatorsByPriority.Union(UnaryOperators).Union(AssignationOperators).ToList();
            Operators.Remove("?");
            Operators.Remove(".");
            ConsiderAsUnary = UnaryOperators.Union(Types).ToList();
            Brackets = OpeningBrackets.Select(b => b + ClosingBrackets[OpeningBrackets.IndexOf(b)]).ToList();
            LexemesOfTokenType = new Dictionary<TokenType, List< string >>
            {
                { TokenType.OpeningBracket, OpeningBrackets},
                { TokenType.ClosingBracket, ClosingBrackets},
                { TokenType.Punctuation, Punctuation},
                { TokenType.ReservedWord, ReservedWords},
                { TokenType.Operator, Operators},
                { TokenType.Quote, Quotes}
            };
        }

        //Semantic errors
        public string ParseError(string value, VariableType targetType) => $"Cannot convert '{value}' to '{targetType}'";
        public string CastError(VariableType sourceType, VariableType targetType) => $"Cannot convert '{sourceType}' to '{targetType}'";
        public string CannotApplyOperator(string operatorName, VariableType leftType, VariableType rightType) => $"Cannot apply operator '{operatorName}' to '{leftType}' and '{rightType}'";
        public string UnknownVariable(string name) => $"Unknown name '{name}'";
        public string VariableWasAlreadyDefined(string name) => $"Variable '{name}' was already defined";
        public string IndexIsPointer() => "Index of array cannot be a pointer";
		public string NotArray(string name) => $"Cannot apply indexing to '{name}'";
        public string NotPointer(string name) => $"'{name}' is not a pointer";
        public string IndexOutOfBounds() => $"Index out of range";
        public string InvalidInitializer() => "Invalid initializer of array";

    }
}
