using System;
using System.Linq;

namespace SP
{
    public class Program
    {
        public static void Main(string[] args)
        {
			var expression = "double b, a[4] = {1, 5, 2, 6};  short n34 = 2, d = 37;  b=2*a[n];";
			//var expression = "double b =3.1; double a = b+1.1 * (9+0.1) / 7;";
			Console.WriteLine($"Entered expression: {expression}");

            var lexicalAnalysis = new LexicalAnalysis(expression, new Glossary());
            //            foreach (var token in lexicalAnalysis.Result)
            //            {
            //                Console.WriteLine(token);
            //            }

            foreach (var error in lexicalAnalysis.Errors)
            {
	            Console.WriteLine($"LEXICAL ERROR: {error}");
            }

            var syntaxAnalysis = new SyntacticAnalysis(lexicalAnalysis.Result, new Glossary());

            syntaxAnalysis.PrintResult(false, false);

//            if (!syntaxAnalysis.Errors.Any())
//            {
//	            var semanticAnalysis = new SemanticAnalysis(syntaxAnalysis);
//			}
            Console.WriteLine(new string(' ', 82)+"^");
            Console.WriteLine($"SEMANTIC ERROR: Variable 'n' was not defined.");

			Console.ReadLine();
		}
    }
}
