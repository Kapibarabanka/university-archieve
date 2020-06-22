using System;
using System.CodeDom;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;

namespace SP
{
    public class SemanticAnalysis
	{
		public Glossary Glossary { get; }
		public Dictionary<string, IVariable> Variables;
		public Dictionary<int, string> Errors;
        public string AssemblerCode = "";

        private int _firstErrorIndex = -1;
        private int _floatIndex = 10;

		private string _dataSection = "";
        private string _codeSection = "";
        private Variable _lastVariable;

		private HashSet<int> freeRegs = new HashSet<int>{0, 1, 2, 3};

		public SemanticAnalysis(SyntacticAnalysis syntacticAnalysis)
		{
			Errors = new Dictionary<int, string>();
			Variables = new Dictionary<string, IVariable>();
			Glossary = syntacticAnalysis.CurrentGlossary;
			Analyze(syntacticAnalysis.Root);
		}

		public SemanticAnalysis(string expression, Glossary glossary)
		{
			Errors = new Dictionary<int, string>();
			Variables = new Dictionary<string, IVariable>();
			Glossary = glossary;
			var lexicalAnalysis = new LexicalAnalysis(expression, glossary);
			var syntacticAnalysis = new SyntacticAnalysis(lexicalAnalysis.Result, glossary);
			Analyze(syntacticAnalysis.Root);
		}

		protected void Analyze(Node rootNode)
        {
			DoStatement(rootNode);
			if (_lastVariable.Type < VariableType.Float)
			{
				AddIntegerOutput();
			}
			else
			{
				AddFloatOutput();
			}
			AssemblerCode += AssemblerHelper.Prologue;
			AssemblerCode += $"\tCaption db \"{_lastVariable.Name.Substring(4, _lastVariable.Name.Length - 4)} =\", 0\n\n";
			AssemblerCode += _dataSection;
			AssemblerCode += AssemblerHelper.Main;
			AssemblerCode += _codeSection;
			
			AssemblerCode += AssemblerHelper.Epilogue;

            if (!Errors.Any())
            {
                Console.WriteLine("\nNo errors were found\n");
                Console.WriteLine("Assembler code:\n");
                Console.WriteLine(AssemblerCode+"\n\n");

                var writePath = @"D:\University\SP\CourseWork\func.asm";
                try
                {
	                using (StreamWriter sw = new StreamWriter(writePath, false, System.Text.Encoding.Default))
	                {
		                sw.WriteLine(AssemblerCode);
	                }

	                Console.WriteLine($"Code is written to file '{writePath}'");
                }
                catch (Exception e)
                {
	                Console.WriteLine(e.Message);
                }
			}
            else
            {
                PrintErrors();
            }
        }

        protected void DoStatement(Node node)
        {
	        if (node.Type == NodeType.Root)
	        {
		        DoStatement(node.Left ?? node.Right);
		        return;
	        }

			if (node.Value == ";")
            {
	            DoStatement(node.Left);
                if (node.Right != null) DoStatement(node.Right);
                return;
            }

            if (node.Type == NodeType.Type && node.Parent.Type != NodeType.AssignationOperator)
            {
                HandleType(node, out var _var);
                return;
            }

            if (node.Type == NodeType.AssignationOperator) HandleAssignationOperator(node);
		}

		protected void AddError(int index, string error)
        {
            Errors.Add(index, error);
            if (_firstErrorIndex == -1) _firstErrorIndex = index;
        }

        protected void PrintErrors()
        {
            var error = Errors[_firstErrorIndex];
            var zeroRow = new string(' ', SyntacticAnalysis.ExprLabel.Length + _firstErrorIndex) + "^";
            var firstRow = "SEMANTIC  ERROR: " + error;
            Console.WriteLine(zeroRow + "\n" + firstRow);
        }

		protected VariableType HandleType(Node node, out IVariable variable)
		{
            var type = GetType(node, out node);
			while (node.Value == ",")
			{
				if (node.Left.Type == NodeType.AssignationOperator)
				{
					CreateVariable(node.Left.Left, type);
					HandleAssignationOperator(node.Left, type);
				}
				else
				{
					CreateVariable(node.Left, type);
				}
				node = node.Right;
			}
			if (node.Type == NodeType.AssignationOperator)
			{
				variable = CreateVariable(node.Left, type);
				HandleAssignationOperator(node, type);
			}
			else
			{
				variable = CreateVariable(node, type);
			}
			return type;
        }

        protected IVariable CreateVariable(Node currentNode, VariableType type)
        {
            IVariable newVariable = new Variable("", VariableType.Error, -1);
            var assemblerSize = "";
            if (currentNode.Type == NodeType.Pointer && currentNode.Value == "*")
            {
	            var pointerName = currentNode.Left.Value;

				if (Variables.Keys.Contains(pointerName))
	            {
					AddError(currentNode.Left.StartPosition, Glossary.VariableWasAlreadyDefined(pointerName));
	            }
                newVariable = new Pointer(pointerName, type, -1);
                Variables.Add(currentNode.Left.Value, newVariable);
                assemblerSize = AssemblerHelper.SizesInAssembler[VariableType.Pointer];
                AddData($"{newVariable.Name} {assemblerSize} ?\t\t\t; {type} *{pointerName}");
                return newVariable;
            }

            if (currentNode.Type == NodeType.Indexer)
            {
	            var arrayName = currentNode.Left.Value;
				if (Variables.Keys.Contains(arrayName))
                {
                    AddError(currentNode.Left.StartPosition, Glossary.VariableWasAlreadyDefined(arrayName));
				}

                if (TryGetIndex(currentNode.Right, out var length))
                {
                    newVariable = new Array(arrayName, type, length);
                    Variables.Add(currentNode.Left.Value, newVariable);
                    assemblerSize = AssemblerHelper.SizesInAssembler[type];
					AddData($"{newVariable.Name} {assemblerSize} {length} dup(?)\t\t; {type} *{arrayName}[{length}]");
                }

                return newVariable;
            }

            var variableName = currentNode.Value;

            if (Variables.Keys.Contains(variableName))
            {
	            AddError(currentNode.StartPosition, Glossary.VariableWasAlreadyDefined(variableName));
            }
            newVariable = new Variable(variableName, type, -1);
            assemblerSize = AssemblerHelper.SizesInAssembler[type];
            AddData($"{newVariable.Name} {assemblerSize} ?\t\t\t; {type} {variableName}");
            Variables[variableName] = newVariable;
            return newVariable;
            
        }

        protected VariableType GetType(Node node, out Node nameNode)
        {
            var stringType = "";
            while (node.Type == NodeType.Type)
            {
                stringType += node.Value + " ";
                node = node.Left;
            }
            stringType = stringType.Trim();
            nameNode = node;
            return IdentifyType(stringType);

             VariableType IdentifyType(string type)
            {
                if (type == "bool") return VariableType.Bool;
                if (type == "char") return VariableType.Char;
                if (type == "int" || type == "signed int" || type == "signed") return VariableType.Int;
                if (type == "unsigned int" || type == "unsigned") return VariableType.UnsignedInt;
                if (type == "short" || type == "short int" || type == "signed short int" || type == "signed short") return VariableType.Short;
                if (type == "unsigned short" || type == "unsigned short int") return VariableType.UnsignedShort;
                if (type == "long" || type == "long int" || type == "signed long int" || type == "signed long") return VariableType.Long;
                if (type == "long short" || type == "unsigned long int") return VariableType.UnsignedLong;
                if (type == "double") return VariableType.Double;
                if (type == "float") return VariableType.Float;
                return VariableType.Error;
            }
        }

        protected void HandleAssignationOperator(Node node, VariableType type = VariableType.Void)
        {
            var targetType = VariableType.Error;
            IVariable targetVariable = new Variable("", VariableType.Error, -1);
            Variable sourceVariable;
			if(node.Left.Type == NodeType.Type || type != VariableType.Void && node.Left.Type == NodeType.Indexer)
            {
	            if (type == VariableType.Void)
	            {
		            targetType = HandleType(node.Left, out targetVariable);
	            }
	            else
	            {
		            targetType = type;
		            targetVariable = GetVariableByName(node.Left.Left);
	            }

                if (targetVariable is Array array)
                {
	                if (node.Right.Value != "{}")
	                {
						AddError(node.Right.StartPosition, Glossary.InvalidInitializer());
						return;
	                }

	                var currentIndex = -1;
	                var currentNode = node.Right.Left;
	                while (currentNode?.Value == ",")
	                {
		                if (currentNode.Left != null)
		                {
			                currentIndex++;
			                var elem = array.GetAtIndex(currentIndex);
			                sourceVariable = GetValue(currentNode.Left);
			                if (sourceVariable == null) return;
			                if (!TryCast(sourceVariable.Type, targetType))
			                {
				                AddError(currentNode.Left.StartPosition, Glossary.CastError(sourceVariable.Type, targetType));
				                return;
			                }
			                if (sourceVariable is Variable elemVariable && sourceVariable.IsTemp)
			                {
								Mov(elem, elemVariable);
			                }
		                }
						currentNode = currentNode.Right;
	                }

	                if (currentNode != null)
	                {
		                currentIndex++;
						if(currentIndex >= array.Length) return;
		                var elem = array.GetAtIndex(currentIndex);
		                sourceVariable = GetValue(currentNode);
		                if (sourceVariable == null) return;
		                if (!TryCast(sourceVariable.Type, targetType))
		                {
			                AddError(currentNode.StartPosition, Glossary.CastError(sourceVariable.Type, targetType));
			                return;
		                }
		                if (sourceVariable is Variable elemVariable && sourceVariable.IsTemp)
		                {
							Mov(elem, elemVariable);
							return;
		                }
						AddError(currentNode.StartPosition, Glossary.InvalidInitializer());
		                return;
	                }
                }
                else
                {
					_lastVariable = (Variable)targetVariable;
				}
             }

			else if (node.Left.Type == NodeType.Name || type != VariableType.Void)
            {
				targetVariable = GetVariableByName(node.Left);
                if (targetVariable is Pointer pointer)
                {
                    targetType = VariableType.Pointer;
                }
                else
                {
                    targetType = targetVariable?.Type ?? VariableType.Error;
                }
            }

			else if (node.Left.Type == NodeType.Indexer)
            {
                if (!(GetVariableByName(node.Left.Left) is Array array))
                {
                    AddError(node.StartPosition, Glossary.NotArray(node.Left.Value));
                    return;
                }
				var arrayMember = GetArrayMember(node.Left);
				targetType = array.Type;
				if (arrayMember != null)
				{
					targetVariable = arrayMember;
				}
                
            }

			else if (node.Left.Type == NodeType.Pointer)
            {
                if (node.Value == "*")
                {
                    if (!(GetVariableByName(node.Left) is Pointer pointer))
                    {
                        AddError(node.StartPosition, Glossary.NotPointer(node.Left.Value));
                        return;
                    }

                    targetType = pointer.Type;
                }
            }

			sourceVariable = GetValue(node.Right);
			if (sourceVariable == null || targetVariable == null) return;
			if (!TryCast(sourceVariable.Type, targetVariable.Type))
			{
				AddError(node.StartPosition, Glossary.CastError(sourceVariable.Type, targetType));
				return;
			}

			_lastVariable = (Variable)targetVariable;
//			if (targetVariable.Type > VariableType.LongLong)
//			{
//				if (sourceVariable.IsFloat)
//				{
//					AddCode($"fld float_const{sourceVariable.Reg}");
//				}
//				else
//				{
//					AddCode($"fild {sourceVariable.Name}");
//				}
//				AddCode($"fstp {targetVariable.Name}");
//				return;
//			}
			Mov( (Variable) targetVariable, sourceVariable);
        }

        protected Variable GetValue(Node node)
        {
	        if (TryConvertToVariable(node, out var variable))
	        {
		        var numVariable = (Variable) variable;
		        if (variable.Name == "" && !numVariable.IsFloat)
		        {
					AddBinAction("mov", variable.Reg, numVariable);
					freeRegs.Remove(variable.Reg);
		        }
		        return numVariable;
	        }
	        switch (node.Type)
	        {
		        case NodeType.UnaryOperator:
		        {
			        switch (node.Value)
			        {
				        case "-":
				        {
					        var child = GetValue(node.Left ?? node.Right);
					        var regIndex = PickReg();
					        var reg = AssemblerHelper.Registers_4b[regIndex];
					        AddCode($"xor {reg}, {reg}");
					        AddBinAction("sub", regIndex, child);
					        return new Variable("", child.Type, regIndex);
				        }
				        case "+":
				        {
					        var child = GetValue(node.Left ?? node.Right);
					        return child;
				        }
			        }

			        break;
		        }
		        case NodeType.BinaryOperator:
		        {
			        var right = GetValue(node.Right);
					var left = GetValue(node.Left);
			        switch (node.Value)
			        {
				        case "-":
				        {
					        return AddBinAction("sub", left, right);
				        }
				        case "+":
				        {
					        return AddBinAction("add", left, right);
				        }
				        case "*":
				        {
					        return AddBinAction("imul", left, right);
				        }
				        case "/":
				        {
					        return AddBinAction("div", left, right);
				        }
						}
					
			        break;
					}
	        }
			return new Variable("", VariableType.Error, -100);
        }

		protected VariableType TypesToBigger(VariableType left, VariableType right)
        {
	        if (left > right) return left;
	        return right;
        }

        protected bool TryConvertToVariable(Node node, out IVariable variable)
        {
			variable = new Variable("", VariableType.Error, -1);
            switch (node.Type)
            {
                case NodeType.CharLiteral:
                {
	                var reg = PickReg();
					if (char.TryParse(node.Value, out var charValue))
                    {
                        variable = new Variable("", VariableType.Char, reg, charValue);
                    }
                    else
                    {
						AddError(node.StartPosition, Glossary.ParseError(node.Value, VariableType.Char));
						variable = null;
						return false;
					}

                    break;
                }

                case NodeType.NumericalConstant:
                {
					if (short.TryParse(node.Value, out var shortValue))
                    {
	                    var reg = PickReg();
						variable = new Variable("", VariableType.Short, reg, shortValue);
                    }

                    else if (ushort.TryParse(node.Value, out var ushortValue))
                    {
	                    var reg = PickReg();
						variable = new Variable("", VariableType.UnsignedShort, reg, ushortValue);
                    }

                    else if (int.TryParse(node.Value, out var intValue))
                    {
	                    var reg = PickReg();
						variable = new Variable("", VariableType.Int, reg, intValue);
                    }

                    else if (uint.TryParse(node.Value, out var uintValue))
                    {
	                    var reg = PickReg();
						variable = new Variable("", VariableType.UnsignedInt, reg, uintValue);
                    }

                    else if (long.TryParse(node.Value, out var longValue))
                    {
	                    var reg = PickReg();
						variable = new Variable("", VariableType.Long, reg, longValue);
                    }

                    else if (ulong.TryParse(node.Value, out var ulongValue))
                    {
	                    var reg = PickReg();
						variable = new Variable("", VariableType.UnsignedLong, reg, ulongValue);
                    }

                    else if (float.TryParse(node.Value, NumberStyles.AllowDecimalPoint, CultureInfo.InvariantCulture, out var floatValue))
                    {
                        variable = new Variable("", VariableType.Float, _floatIndex, floatValue);
                        AddData($"float_const{_floatIndex++} dd {floatValue.ToString(CultureInfo.InvariantCulture)}");
					}

                    else if (double.TryParse(node.Value, NumberStyles.AllowDecimalPoint, CultureInfo.InvariantCulture, out var doubleValue))
                    {
                        variable = new Variable("", VariableType.Double, _floatIndex, doubleValue);
                        AddData($"float_const{_floatIndex++} dd {doubleValue.ToString(CultureInfo.InvariantCulture)}");
					}
                    break;
                }

                case NodeType.Name:
                {
                    variable = GetVariableByName(node);
                    return true;
                }

                case NodeType.Pointer:
                {
                    variable = GetVariableByName(node.Left ?? node.Right);
                    return true;
                }

                case NodeType.Indexer:
                {
	                variable = GetArrayMember(node);
	                return true;
                }

                default:
                {
	                variable = new Variable("", VariableType.Error, -1);
	                return false;
				}
            }
            return true;
        }

        protected IVariable GetVariableByName(Node node)
        {
	        if (Variables.ContainsKey(node.Value))
	        {
		        return Variables[node.Value];
	        }
			AddError(node.StartPosition, Glossary.UnknownVariable(node.Value));
			return null;
        }

        protected Variable GetArrayMember(Node node)
        {
	        var name = node.Left.Value;
            if (Variables.ContainsKey(name))
	        {
		        if (Variables[name] is Array array)
		        {
			        var indexVariable = GetValue(node.Right);
			        var size = AssemblerHelper.SizesInBytes[array.GetAtIndex(0).Type];
					var sizeVariable = new Variable("", VariableType.Int, -1, size);
					var indexReg = indexVariable.Reg == -1 ? PickReg() : indexVariable.Reg;
					if (indexVariable.Reg == -1)
					{
						AddBinAction("mov", indexReg, indexVariable);
					}
					
					AddBinAction("imul", indexReg, sizeVariable);
					return new Variable($"dword ptr[{array.Name} + {AssemblerHelper.Registers_4b[indexReg]}]", array.GetAtIndex(0).Type, indexReg);
				}
		        else
		        {
			        AddError(node.StartPosition, Glossary.NotArray(name));
				}
		        return null;
	        }
	        AddError(node.Left.StartPosition, Glossary.UnknownVariable(node.Value));
	        return null;
        }

        protected bool TryGetIndex(Node node, out int index)
        {
			if (!TryConvertToVariable(node, out var indexVariable))
	        {
				AddError(node.StartPosition, "Error index");
		        index = -1;
		        return false;
	        }
            if (indexVariable is Pointer && node.Value != "*")
            {
                AddError(node.StartPosition, Glossary.IndexIsPointer());
                index = -1;
                return false;
            }
            if (TryCast( indexVariable.Type, VariableType.Int))
	        {
		        if (indexVariable is Variable exactVar)
		        {
			        var isInt = int.TryParse(exactVar.Value.ToString(), out index);
			        if (isInt) return true;
		        }
	        }
	        AddError(node.StartPosition, 
		        Glossary.CastError(indexVariable.Type, VariableType.Int));
		        
	        index = -1;
	        return false;
		}

		
		protected bool TryCast(VariableType sourceType, VariableType targetType)
        {
            if (sourceType == VariableType.Pointer &&
                (targetType == VariableType.Float || targetType == VariableType.Double))
            {
                return false;
            }
            if (targetType == VariableType.Pointer &&
                (sourceType == VariableType.Float || sourceType == VariableType.Double))
            {
                return false;
            }
            if (sourceType <= VariableType.Double && targetType <= VariableType.Double && targetType >= sourceType)
            {
                return true;
            }
            return false;
		}

		private void AddData(string line)
		{
			_dataSection += $"\t{line}\n";
		}

		private void AddCode(string line)
		{
			_codeSection += $"\t{line}\n";
		}

		private void Mov(Variable target, Variable source)
		{
			if (!target.IsTemp)
			{
				if (!source.IsTemp)
				{
					VarToVar(target, source);
					return;
				}

				if (target.IsFloat)
				{
					if (source.IsFloat)
					{
						AddCode($"fld float_const{source.Reg}");
					}
					else
					{
						if (source.IsTemp)
						{
							AddCode($"mov int_buf, {source.Value}");
							AddCode($"fild int_buf");
						}
						else
						{
							AddCode($"fild {source.Name}");
						}
						FreeReg(source.Reg);
					}
					AddCode($"fstp {target.Name}");
					return;
				}
				var targetType = AssemblerHelper.SizesInAssembler[target.Type];
				var sourceReg = AssemblerHelper.Registers[targetType][source.Reg];
				AddCode($"mov {target.Name}, {sourceReg}");
				FreeReg(source.Reg);
			}
		}

		private Variable AddBinAction(string action, Variable left, Variable right)
		{
			var resultType = action == "div" ? VariableType.Double : TypesToBigger(left.Type, right.Type);

			if (resultType > VariableType.LongLong)
			{
				var resultVariable = new Variable("", VariableType.Float, _floatIndex);
				AddData($"float_const{_floatIndex++} dd 0");
				if (action == "imul") action = "mul";
				if (left.IsFloat)
				{
					if (left.IsTemp)
					{
						AddCode($"fld float_const{left.Reg}");
					}
					else
					{
						AddCode($"fld {left.Name}");
					}
				}
				else
				{
					if (left.IsTemp)
					{
						AddCode($"mov int_buf, {left.Value}");
						AddCode($"fild int_buf");
					}
					else
					{
						AddCode($"fild {left.Name}");
					}
				}
				if (right.IsFloat)
				{
					if (right.IsTemp)
					{
						AddCode($"fld float_const{right.Reg}");
					}
					else
					{
						AddCode($"fld {right.Name}");
					}
				}
				else
				{
					if (right.IsTemp)
					{
						AddCode($"mov int_buf, {right.Value}");
						AddCode($"fild int_buf");
					}
					else
					{
						AddCode($"fild {right.Name}");
					}
				}
				AddCode($"f{action}");
				AddCode($"fstp float_const{resultVariable.Reg}");
				FreeReg(left.Reg);
				FreeReg(right.Reg);
				return resultVariable;
			}

			string leftValue;
			var leftIndex = left.Reg;
			if (left.IsTemp)
			{
				var leftType = AssemblerHelper.SizesInAssembler[resultType];
				leftValue = AssemblerHelper.Registers[leftType][left.Reg];
			}
			else
			{
				leftIndex = PickReg();
				var bigType = AssemblerHelper.SizesInAssembler[resultType];
				var bigReg = AssemblerHelper.Registers[bigType][leftIndex];
				if (left.Type == resultType)
				{
					AddCode($"mov {bigReg}, {left.Name}");
				}
				else
				{
					var smallType = AssemblerHelper.SizesInAssembler[resultType];
					var smallReg = AssemblerHelper.Registers[smallType][leftIndex];
					AddCode($"mov {smallReg}, {left.Name}");
				}
				leftValue = bigReg;
			}

			string rightValue;
			var rightIndex = right.Reg;
			if (right.IsTemp)
			{
				var rightType = AssemblerHelper.SizesInAssembler[resultType];
				rightValue = AssemblerHelper.Registers[rightType][right.Reg];
			}
			else
			{
				if (right.Type == resultType)
				{
					rightValue = right.Name;
				}
				else
				{
					var smallType = AssemblerHelper.SizesInAssembler[resultType];
					rightIndex = PickReg();
					var smallReg = AssemblerHelper.Registers[smallType][rightIndex];
					AddCode($"mov {smallReg}, {right.Name}");
					var bigType = AssemblerHelper.SizesInAssembler[resultType];
					var bigReg = AssemblerHelper.Registers[bigType][rightIndex];
					rightValue = bigReg;
				}
			}
			AddCode($"{action} {leftValue}, {rightValue}");
			FreeReg(rightIndex);
			AddCode("\n");
			return new Variable("", resultType, leftIndex);
		}

		private void AddBinAction(string action, int reg, Variable source)
		{
			freeRegs.Remove(reg);
			source.Reg = reg;
			var sourceType = AssemblerHelper.SizesInAssembler[source.Type];
			var targetReg = AssemblerHelper.Registers[sourceType][reg];
			var sourceValue = source.IsTemp ? source.Value : source.Name;
			AddCode($"{action} {targetReg}, {sourceValue}");
		}

		private void VarToVar(Variable target, Variable source)
		{
			if (target.IsFloat)
			{
				AddCode(source.IsFloat ? $"fld {source.Name}" : $"fild {source.Name}");
				AddCode($"fstp {target.Name}");
				return;
			}
			var regIndex = PickReg();
			var targetType = AssemblerHelper.SizesInAssembler[target.Type];
			var targetReg = AssemblerHelper.Registers[targetType][regIndex];

			var sourceType = AssemblerHelper.SizesInAssembler[source.Type];
			var sourceReg = AssemblerHelper.Registers[sourceType][regIndex];

			AddCode($"mov {sourceReg}, {source.Name}");
			AddCode($"mov {target.Name}, {targetReg}");
		}

		private int PickReg()
		{
			if (freeRegs.Any())
			{
				var r = freeRegs.First();
				freeRegs.Remove(r);
				AddCode("\n");
				AddCode($"xor {AssemblerHelper.Registers_4b[r]}, {AssemblerHelper.Registers_4b[r]}");
				return r;
			}

			return 3;
		}
			

		protected Node SkipUnaryToChild(Node current)
		{
			while (Glossary.ConsiderAsUnary.Contains(current.Value) && current.Children.Any())
			{
				current = current.Children[0];
			}
			return current;
		}

		private void FreeReg(int reg)
		{
			if (reg != -1 && reg < 4)
			{
				freeRegs.Add(reg);
			}
		}

		private void AddIntegerOutput()
		{
			if (!_lastVariable.IsTemp)
			{
				AddCode("\n");
				AddCode("invoke crt_printf, addr Caption");
				AddCode($"invoke crt_printf, addr int_fmt, {_lastVariable.Name}");
			}
		}

		private void AddFloatOutput()
		{
			if (!_lastVariable.IsTemp)
			{
				AddCode($"fld {_lastVariable.Name}");
				AddCode($"fstp buff");
				AddCode("\n");
				AddCode("invoke crt_printf, addr Caption");
				AddCode($"invoke crt_printf, addr flt_fmt, buff");
			}
		}
	}
}
