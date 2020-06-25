using System;
using System.Collections.Generic;
using System.Linq;
using static SP.Glossary;

namespace SP
{
    public enum NodeType
    {
        Root,
        Empty,
        Quotes,
        Brackets,
		Indexer,
		FunctionCall,
        Name,
        NumericalConstant,
        StringLiteral,
		CharLiteral,
        Punctuation,
        UnaryOperator,
        BinaryOperator,
		AssignationOperator,
        Pointer,
        Type,
        ErrorLexeme,
		Condition,
        BlockOperator,
        Return,
    }

    public class Node
	{
        public string Value;
		public NodeType Type;
		public Node Parent;

		public List<Node> Children;

        public Node Left => Children.Count > 0 ? Children[0] : null;
        public Node Right => Children.Count > 1 ? Children[1] : null;

        public int StartPosition;
        public int EndPosition;

		public string PreviousToken;
        public string NextToken;

        public List<SyntacticErrorType> Errors;

        public Node(string value, NodeType type, Node parent)
		{
			Value = value;
			Type = type;
			Parent = parent;
			Errors = new List<SyntacticErrorType>();
			parent?.Children.Add(this);
			Children = new List<Node>();
        }

		public override string ToString()
        {
            var children = new List<Node> {Left, Right};
            if (children.All(c => c == null)) return $"{Value}";
			var result = $"{Value} -> {{ ";
            foreach (var child in children)
            {
                result += $"| {child} |";
            }
            return result + " }}";
		}

        public List<Node> ToList()
        {
            var result = new List<Node>{this};

            if (Left != null) result.AddRange(Left.ToList());
            if (Right != null) result.AddRange(Right.ToList());

            return result;
        }

        public void AddChild(Node newNode)
        {
            Children.Add(newNode);
            newNode.Parent = this;
        }

        public void InsertBeforeChild(Node oldChild, Node newChild)
        {
			var index = Children.IndexOf(oldChild);
			Children[index] = newChild;
			newChild.Parent = this;
			newChild.AddChild(oldChild);
		}

        public void RemoveChild(Node child)
        {
	        if (child.Children.Count == 1)
	        {
		        var index = Children.IndexOf(child);
		        Children[index] = child.Children[0];
		        child.Children[0].Parent = this;
			}
        }

        public void Update(string value, NodeType type)
        {
            Value = value;
            Type = type;
        }

        public Node FindUp(string value)
        {
            var currentNode = this;
            while (currentNode.Type != NodeType.Root)
            {
                if (currentNode.Value == value) return currentNode;
                currentNode = currentNode.Parent;
            }

            return null;
        }

        public void AddError(SyntacticErrorType syntacticError)
        {
			Errors.Add(syntacticError);
        }

        public void ResolveError(SyntacticErrorType syntacticError)
        {
	        Errors.Remove(syntacticError);
        }
		
        public bool CanBeRvalue => Type == NodeType.Name || Type == NodeType.NumericalConstant ||
                                   (Type == NodeType.Indexer && Value == "[]") || Type == NodeType.FunctionCall ||
                                   Type == NodeType.Quotes ||
                                   Glossary.MathOperators.Contains(Value);

        public bool CanBeLvalue => Type == NodeType.Name || Type == NodeType.Indexer ||
                                   Value == "." && Right.Type == NodeType.Name || Type == NodeType.Type;
	}

    public static class BTreePrinter
    {
        class NodeInfo
        {
            public Node Node;
            public string Text;
            public int StartPos;
            public int Size { get { return Text.Length; } }
            public int EndPos { get { return StartPos + Size; } set { StartPos = value - Size; } }
            public NodeInfo Parent, Left, Right;
        }

        public static void Print(this Node root, string textFormat = "0", int spacing = 1, int topMargin = 2, int leftMargin = 2)
        {
            if (root == null) return;
            int rootTop = Console.CursorTop + topMargin;
            var last = new List<NodeInfo>();
            var next = root;
            for (int level = 0; next != null; level++)
            {
                var item = new NodeInfo { Node = next, Text = next.Value };
                if (level < last.Count)
                {
                    item.StartPos = last[level].EndPos + spacing;
                    last[level] = item;
                }
                else
                {
                    item.StartPos = leftMargin;
                    last.Add(item);
                }
                if (level > 0)
                {
                    item.Parent = last[level - 1];
                    if (next == item.Parent.Node.Left)
                    {
                        item.Parent.Left = item;
                        item.EndPos = Math.Max(item.EndPos, item.Parent.StartPos - 1);
                    }
                    else
                    {
                        item.Parent.Right = item;
                        item.StartPos = Math.Max(item.StartPos, item.Parent.EndPos + 1);
                    }
                }
                next = next.Left ?? next.Right;
                for (; next == null; item = item.Parent)
                {
                    int top = rootTop + 2 * level;
                    Print(item.Text, top, item.StartPos);
                    if (item.Left != null)
                    {
                        Print("/", top + 1, item.Left.EndPos);
                        Print("_", top, item.Left.EndPos + 1, item.StartPos);
                    }
                    if (item.Right != null)
                    {
                        Print("_", top, item.EndPos, item.Right.StartPos - 1);
                        Print("\\", top + 1, item.Right.StartPos - 1);
                    }
                    if (--level < 0) break;
                    if (item == item.Parent.Left)
                    {
                        item.Parent.StartPos = item.EndPos + 1;
                        next = item.Parent.Node.Right;
                    }
                    else
                    {
                        if (item.Parent.Left == null)
                            item.Parent.EndPos = item.StartPos - 1;
                        else
                            item.Parent.StartPos += (item.StartPos - 1 - item.Parent.EndPos) / 2;
                    }
                }
            }
            Console.SetCursorPosition(0, rootTop + 2 * last.Count - 1);
        }

        private static void Print(string s, int top, int left, int right = -1)
        {
            Console.SetCursorPosition(left, top);
            if (right < 0) right = left + s.Length;
            while (Console.CursorLeft < right) Console.Write(s);
        }
    }
}
