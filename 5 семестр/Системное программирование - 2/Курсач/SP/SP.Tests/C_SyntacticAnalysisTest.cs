using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Microsoft.VisualStudio.TestTools.UnitTesting;

namespace SP.Tests
{
	[TestClass]
	public class C_SyntacticAnalysisTest
	{
		[TestMethod]
		public void TypesTest()
		{
			var expression = "int b=2*a[n]; unsigned long b = d; int[] a = 0;";

			var c = new SyntacticAnalysis(expression, new Glossary());

			Assert.IsTrue(c.OldErrors.Count == 0);
		}

		[TestMethod]
		public void IfTest()
		{
			var expression = "if a > b  a = 8;";

			var c = new SyntacticAnalysis(expression, new Glossary());

			Assert.IsTrue(c.OldErrors.Count == 1);
		}

		[TestMethod]
		public void ElseTest()
		{
			var expression = "else {a = 0;}";

			var c = new SyntacticAnalysis(expression, new Glossary());

			Assert.IsTrue(c.OldErrors.Count == 1);
		}
	}
}
