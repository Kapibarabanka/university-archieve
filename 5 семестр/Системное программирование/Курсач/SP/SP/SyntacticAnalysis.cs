using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.Remoting.Messaging;
using System.Text;
using System.Threading.Tasks;

namespace SP
{
	public enum SyntacticErrorType
	{
		BracketNotClosed,
		QuoteNotClosed,
		ArrayNameExpectedBeforeIndexer,
		IndexExpected,
		BinaryOperatorMustTakeTwoOperands,
		LeftSideOfAssignationOperator,
		SemicolonExpected,

		ColonExpected,
		BracketsExpectedAfterIf,

		UnexpectedToken
	}
	public class SyntacticAnalysis
    {
		public static string ExprLabel = "Entered expression: ";

		public Glossary CurrentGlossary { get; }

		public Dictionary<int, string> Errors;

		public Node Root;

		public delegate Node Handler(Token token, Node lastNode);

		public Dictionary<TokenType, Handler> TokenTypesHandlers;

		public SyntacticAnalysis(List<Token> tokens, Glossary currentGlossary)
        {
            CurrentGlossary = currentGlossary;
            Errors = new Dictionary<int, string>();
			Initialize();
            Root = Analyze(tokens);
        }

        public SyntacticAnalysis(string expression, Glossary currentGlossary)
        {
            CurrentGlossary = currentGlossary;
            Errors = new Dictionary<int, string>();
			Initialize();
            var lexicalAnalysis = new LexicalAnalysis(expression, currentGlossary);
            Root = Analyze(lexicalAnalysis.Result);
        }

        public Node Analyze(List<Token> tokens)
        {
	        var rootNode = new Node("root", NodeType.Root, null);
	        var lastNode = rootNode;
	        for (var i = 0; i < tokens.Count; i++)
	        {
		        var token = tokens[i];
		        PreHandlerCheck(token, lastNode);
		        lastNode = TokenTypesHandlers[token.Type](token, lastNode);
		        if (!IsUpdated(lastNode))
		        {
			        lastNode.StartPosition = token.StartPosition;
			        lastNode.PreviousToken = i == 0 ? null : tokens[i - 1].Value;
			        lastNode.NextToken = i + 1 == tokens.Count ? null : tokens[i + 1].Value;
		        }
		        else
		        {
			        lastNode.EndPosition = token.StartPosition + token.Value.Length;
		        }
		        PostHandlerCheck(lastNode);
	        }

	        Errors = GetErrors(rootNode);
	        return rootNode;
        }

		protected void PreHandlerCheck(Token token, Node lastNode)
        {
	        if (CurrentGlossary.BinaryOperatorsByPriority.Contains(lastNode.Value) && CanBeRvalue(token) ||
	            lastNode.Left?.Type == NodeType.Indexer && token.Value == "{")
		        lastNode.ResolveError(SyntacticErrorType.BinaryOperatorMustTakeTwoOperands);
			if (token.Value == "(" && lastNode.Value == "if")
				lastNode.ResolveError(SyntacticErrorType.BracketsExpectedAfterIf);
        }

		protected void PostHandlerCheck(Node lastNode)
		{
			if (lastNode.Parent.Type == NodeType.Name && lastNode.Type != NodeType.FunctionCall || lastNode.Parent.Type == NodeType.NumericalConstant ||
			    lastNode.Parent.Children.Count > 2)
			{
				lastNode.AddError(SyntacticErrorType.UnexpectedToken);
			}
		}

		#region Handlers

		protected Node HandleOpeningBracket(Token token, Node lastNode)
		{
			Node newNode;
			if (token.Value == "[")
			{
				newNode = HandleIndexer(token, lastNode);
			}
			else if (token.Value == "(" && lastNode.Type == NodeType.Name)
			{
				newNode = HandleFunctionCall(token, lastNode);
			}
			else
			{
				newNode = new Node(token.Value, NodeType.Brackets, lastNode);
			}
			newNode.AddError(SyntacticErrorType.BracketNotClosed);
			return newNode;
		}

		protected Node HandleIndexer(Token token, Node lastNode)
		{
			var newNode = HandleBinaryOperator(token, lastNode);
			newNode.Update(token.Value, NodeType.Indexer);
			if (!lastNode.CanBeRvalue) newNode.AddError(SyntacticErrorType.ArrayNameExpectedBeforeIndexer);
			return newNode;
		}

		protected Node HandleFunctionCall(Token token, Node lastNode)
		{
			var newNode = new Node(token.Value, NodeType.FunctionCall, null);
			lastNode.Parent.InsertBeforeChild(lastNode, newNode);
			return newNode;
		}

		protected Node HandleClosingBracket(Token token, Node lastNode)
		{
			var correspondingOpeningBracket = CurrentGlossary.Brackets.First(b => b.Contains(token.Value))[0].ToString();
			var openingNode = lastNode.FindUp(correspondingOpeningBracket);
			if (openingNode != null)
			{
				openingNode.Value += token.Value;
				openingNode.ResolveError(SyntacticErrorType.BracketNotClosed);
				if (openingNode.Type == NodeType.Brackets && openingNode.Value != "{}")
				{
					var child = openingNode.Left ?? openingNode.Right;
					openingNode.Parent.RemoveChild(openingNode);
					return child;
				}
				return openingNode;
			}
			var newNode = new Node(token.Value, NodeType.Brackets, null);
			newNode.AddError(SyntacticErrorType.UnexpectedToken);
			lastNode.Parent.InsertBeforeChild(lastNode, newNode);
			return newNode;
		}

		protected Node HandleNumericalConstant(Token token, Node lastNode)
		{
			return new Node(token.Value, NodeType.NumericalConstant, lastNode);
		}

		protected Node HandleName(Token token, Node lastNode)
		{
			return new Node(token.Value, NodeType.Name, lastNode);
		}

		protected Node HandleQuote(Token token, Node lastNode)
		{
			var openingNode = lastNode.FindUp(token.Value);
			if (openingNode != null)
			{
				openingNode.ResolveError(SyntacticErrorType.QuoteNotClosed
);
				openingNode.Value += token.Value;
				openingNode.Left.Update(openingNode.Left.Value,
					token.Value == "'" ? NodeType.CharLiteral : NodeType.StringLiteral);
				return openingNode;
			}

			var newNode = new Node(token.Value, NodeType.Quotes, lastNode);
			newNode.AddError(SyntacticErrorType.QuoteNotClosed);
			return newNode;
		}

		protected Node HandleErrorLexeme(Token token, Node lastNode)
		{
			if (lastNode.Value == "\"") return new Node(token.Value, NodeType.StringLiteral, lastNode);
			if (lastNode.Value == "'") return new Node(token.Value, NodeType.CharLiteral, lastNode);
			return new Node(token.Value, NodeType.ErrorLexeme, lastNode);
		}

		protected Node HandleOperator(Token token, Node lastNode)
		{
			if (CurrentGlossary.IncDecOperators.Contains(token.Value) ||
			    CurrentGlossary.UnaryOperators.Contains(token.Value) && !lastNode.CanBeRvalue) return HandleUnaryOperator(token, lastNode);
			if (CurrentGlossary.BinaryOperatorsByPriority.Contains(token.Value)) return HandleBinaryOperator(token, lastNode);
			var newNode = new Node(token.Value, NodeType.Empty, lastNode);
			newNode.AddError(SyntacticErrorType.UnexpectedToken);
			return newNode;
		}

		protected Node HandleUnaryOperator(Token token, Node lastNode)
		{
			var newNode = new Node(token.Value, NodeType.UnaryOperator, lastNode);
			if (CurrentGlossary.Pointers.Contains(token.Value))
			{
				newNode.Update(token.Value, NodeType.Pointer);
			}
			else if (CurrentGlossary.Types.Contains(token.Value))
			{
				newNode.Update(token.Value, NodeType.Type);
			}
			return newNode;
		}

		protected Node HandleBinaryOperator(Token token, Node lastNode)
		{
			if (CurrentGlossary.AssignationOperators.Contains(token.Value))
				return HandleAssignationOperator(token, lastNode);

			var result = new Node(token.Value, NodeType.BinaryOperator, null);
			result.AddError(SyntacticErrorType.BinaryOperatorMustTakeTwoOperands);
			var lastPriority = CurrentGlossary.BinaryOperatorsByPriority.IndexOf(lastNode.Parent.Value);
			var newPriority = CurrentGlossary.BinaryOperatorsByPriority.IndexOf(token.Value);
			if (lastNode.Parent.Type != NodeType.Brackets && lastPriority != -1 && newPriority > lastPriority)
			{
				lastNode.Parent.Parent.InsertBeforeChild(lastNode.Parent, result);
			}
			else
			{
				lastNode.Parent.InsertBeforeChild(lastNode, result);
			}
			return result;
		}

		protected Node HandleAssignationOperator(Token token, Node lastNode)
		{
			var newNode = new Node(token.Value, NodeType.AssignationOperator, null);
			lastNode.Parent.InsertBeforeChild(lastNode, newNode);

			newNode.AddError(SyntacticErrorType.BinaryOperatorMustTakeTwoOperands);
			if (!newNode.Left.CanBeLvalue) newNode.AddError(SyntacticErrorType.LeftSideOfAssignationOperator);
			return newNode;
		}

		protected Node HandleReservedWord(Token token, Node lastNode)
		{
			if (CurrentGlossary.ConsiderAsUnary.Contains(token.Value)) return HandleUnaryOperator(token, lastNode);
			switch (token.Value)
			{
				case "if": return HandleIf(token, lastNode);
				case "else": return HandleElse(token, lastNode);
                case "return": return new Node(token.Value, NodeType.Return, lastNode);
			}

			return lastNode;
		}

        protected Node HandlePunctuation(Token token, Node lastNode)
		{
			switch (token.Value)
			{
				case ";": return HandleSemicolon(token, lastNode);
				case "?": return HandleIf(token, lastNode);
				case ":": return HandleElse(token, lastNode);
				default:
				{
					var newNode = new Node(token.Value, NodeType.Punctuation, lastNode);
					newNode.AddError(SyntacticErrorType.UnexpectedToken);
					return newNode;
				}
			}
		}

        protected Node HandleIf(Token token, Node lastNode)
        {
	        if (token.Value == "?")
	        {
		        var binNode = HandleBinaryOperator(token, lastNode);
		        binNode.Update(token.Value, NodeType.Condition);
		        binNode.AddError(SyntacticErrorType.ColonExpected);
		        return binNode;
	        }
	        var newNode = new Node(token.Value, NodeType.Condition, null);
	        var beforeActionNode = FindBeforeAction(lastNode);
	        if (beforeActionNode != null)
	        {
		        beforeActionNode.AddChild(newNode);
		        newNode.AddError(SyntacticErrorType.BracketsExpectedAfterIf);
	        }
	        else
	        {
		        newNode.AddError(SyntacticErrorType.UnexpectedToken);
		        lastNode.AddChild(newNode);
	        }
	        return newNode;
        }

        protected Node HandleElse(Token token, Node lastNode)
        {
	        var newNode = new Node(token.Value, NodeType.Condition, null);
	        var ifNode = lastNode.FindUp("if");
	        if (ifNode != null)
	        {
		        ifNode.Parent.InsertBeforeChild(ifNode, newNode);
	        }
	        else
	        {
		        lastNode.AddChild(newNode);
		        newNode.AddError(SyntacticErrorType.UnexpectedToken);
	        }

	        return newNode;
        }

        protected Node HandleSemicolon(Token token, Node lastNode)
        {
	        while (lastNode.Parent.Type != NodeType.Root && lastNode.Parent.Value != ";" &&
	               !CurrentGlossary.ReservedWords.Contains(lastNode.Value) &&
	               lastNode.Parent.Value != "{")
	        {
		        lastNode = lastNode.Parent;
	        }

	        var newNode = new Node(token.Value, NodeType.Punctuation, null);
	        lastNode.Parent.InsertBeforeChild(lastNode, newNode);

	        return newNode;
        }

		#endregion

		protected bool IsUpdated(Node node)
		{
			return (node.Type == NodeType.Brackets || node.Type == NodeType.Indexer ||
			        node.Type == NodeType.FunctionCall)
			       && !node.Errors.Contains(SyntacticErrorType.BracketNotClosed);
		}

		protected bool IsIncOrDec(Node node)
        {
            return CurrentGlossary.IncDecOperators.Contains(node.Value) ||
                   (node.Type == NodeType.Name && CurrentGlossary.IncDecOperators.Contains(node.Left.Value));
        }

		protected bool CanBeRvalue(Token token) =>
			token.Type == TokenType.Name || token.Type == TokenType.NumericalConstant ||
			token.Value == "*" ||
			CurrentGlossary.UnaryOperators.Contains(token.Value) ||
			token.Type == TokenType.OpeningBracket && token.Value == "(" ||
			CurrentGlossary.Quotes.Contains(token.Value);

		protected Node FindBeforeAction(Node currentNode)
		{
			if (currentNode.Type == NodeType.Root) return currentNode;
			while (currentNode.Type != NodeType.Root)
			{
				if (CurrentGlossary.BeforeActionMarkers.Contains(currentNode.Value) && currentNode.Right == null)
					return currentNode;
				currentNode = currentNode.Parent;
			}

			return null;
		}

		protected void Initialize()
		{
			TokenTypesHandlers = new Dictionary<TokenType, Handler>
			{
				{TokenType.ClosingBracket, HandleClosingBracket},
				{TokenType.OpeningBracket, HandleOpeningBracket},
				{TokenType.NumericalConstant, HandleNumericalConstant },
				{TokenType.Name, HandleName },
				{TokenType.Operator, HandleOperator },
				{TokenType.Punctuation, HandlePunctuation },
				{TokenType.ReservedWord,HandleReservedWord },
				{TokenType.Quote, HandleQuote },
				{TokenType.ErrorLexeme, HandleErrorLexeme }
			};
		}

		public Dictionary<int, string> GetErrors(Node node)
		{
			var result = new Dictionary<int, string>();
			var leftErrors = node.Left == null ? new Dictionary<int, string>() : GetErrors(node.Left);
			var rightErrors = node.Right == null ? new Dictionary<int, string>() : GetErrors(node.Right);
			foreach (var leftError in leftErrors)
			{
				result.Add(leftError.Key, leftError.Value);
			}
			foreach (var rightError in rightErrors)
			{
				result.Add(rightError.Key, rightError.Value);
			}

			foreach (var nodeError in node.Errors)
			{
				var position = node.StartPosition;
				switch (nodeError)
				{
					case SyntacticErrorType.SemicolonExpected:
						{
							if (node.Type == NodeType.BlockOperator)
							{
								position = node.EndPosition;
							}

							break;
						}
				}
				var zeroRow = new string(' ', ExprLabel.Length + position) + "^";
				var firstRow = "SYNTAX  ERROR: " + nodeError;
				result[position] = zeroRow + "\n" + firstRow;
			}
			return result;
		}

		public void PrintResult(bool noErrorsPrint = false, bool tree = false)
		{
			if (Errors.Any())
			{
				Console.WriteLine(Errors[Errors.Keys.Min()]);
				if (noErrorsPrint) return;
			}

			if (noErrorsPrint)
			{
				Console.WriteLine("\nNo syntactic errors were found\n");
				Root.Print();
			}
			if (tree) Root.Print();
		}

	}
}
