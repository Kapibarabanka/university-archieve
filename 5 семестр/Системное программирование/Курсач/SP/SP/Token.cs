using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SP
{
	public enum TokenType
	{
		OpeningBracket,
		ClosingBracket,
		Operator,
		Quote,
		NumericalConstant,
		Name,
		Punctuation,
		ReservedWord,
		ErrorLexeme
	}
	public class Token
    {
        public string Value;
        public TokenType Type;
        public int StartPosition;

        public Token(string value, TokenType type)
        {
            Value = type == TokenType.ReservedWord || type == TokenType.Operator ? value.ToLower() : value;
            Type = type;
        }

        public override string ToString()
        {
	        return $"{Value} ({Type})";
        }

        //TODO: needs improvement
        public bool CanBeRvalue => Type == TokenType.Name || Type == TokenType.NumericalConstant ||
                                   Type == TokenType.OpeningBracket && Value == "(";
    }
}
