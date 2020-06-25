using System;
using System.Collections.Generic;
using System.Text.RegularExpressions;

namespace SP
{
    public class LexicalAnalysis
    {
        public Glossary CurrentGlossary;
	    public List<Token> Result;
        public List<string> Errors;
	    public LexicalAnalysis(string input, Glossary currentGlossary)
        {
            CurrentGlossary = currentGlossary;
            Errors = new List<string>();
            Result = Analyze(input);
        }
        public List<Token> Analyze(string input)
        {
            foreach (var pair in CurrentGlossary.LexemesOfTokenType)
            {
                pair.Value.Sort(delegate (string x, string y)
                {
                    if (x.Length > y.Length) return -1;
                    if (x.Length < y.Length) return 1;
                    return 0;
                });
            }
            var result = new List<Token>();
            var startIndex = 0;
            while (startIndex < input.Length)
            {
                if (input[startIndex] == ' ')
                {
                    startIndex++;
                    continue;
                }
                var str = input.Substring(startIndex);
                var token = FindFirstToken(str);
				result.Add(token);
				token.StartPosition = startIndex;
                startIndex += token.Value.Length;
            }

            for (var i = 1; i < result.Count; i++)
            {
				if (result[i].Type == TokenType.ErrorLexeme &&
				    !(result[i-1].Type == TokenType.Quote && result[i + 1].Type == TokenType.Quote &&
					  result[i - 1].Value == result[i +1].Value))
				Errors.Add($"Error lexeme ('{result[i].Value}')");
            }

            return result;
        }

        private Token FindFirstToken(string str)
        {
            var first = str.Length;
            var firstDot = str.IndexOf(".");
            foreach (var pair in CurrentGlossary.LexemesOfTokenType)
            {
                foreach (var item in pair.Value)
                {
                    var index = str.IndexOf(item, StringComparison.OrdinalIgnoreCase);
                    if (index == 0) return new Token(str.Substring(0, item.Length), pair.Key);
                    if (index != -1 && index < first && item != ".") first = index;
                }
            }
            var indexOfSpace = str.IndexOf(" ");
            if (indexOfSpace != -1 && indexOfSpace < first) first = indexOfSpace;

            var undefinedPart = str.Substring(0, first);
            if ( IsNumericalConstant(undefinedPart)) return new Token(undefinedPart, TokenType.NumericalConstant);
			if (firstDot != -1 && firstDot < first) undefinedPart = str.Substring(0, firstDot);
			if (IsName(undefinedPart)) return new Token(undefinedPart, TokenType.Name);
            return new Token(undefinedPart, TokenType.ErrorLexeme);
        }

        private static bool IsName(string str)
        {
            return Char.IsLetter(str[0]) || str[0] == '_';
        }

        private static bool IsNumericalConstant(string str)
        {
            Regex regex = new Regex(@"^[0-9]\d*(?:\.\d+)?(?:[f])?$");
            var match = regex.Match(str);
            return match.Success || str == "0";
        }

    }
}
