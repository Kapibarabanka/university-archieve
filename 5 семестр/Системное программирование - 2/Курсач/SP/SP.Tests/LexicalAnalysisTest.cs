using System;
using System.Collections.Generic;
using Microsoft.VisualStudio.TestTools.UnitTesting;
namespace SP.Tests
{
    [TestClass]
    public class LexicalAnalysisTest
    {
        [TestMethod]
        public void C_AnalysisTest()
        {
            var expression = "b = 6;";
            var expectedNames = new List<string>() {"b", "=", "6", ";" };
            var expectedTypes = new List<TokenType>()
            {
                TokenType.Name,
                TokenType.Operator,
                TokenType.NumericalConstant,
                TokenType.Punctuation
            };

            var analysis = new LexicalAnalysis(expression, new Glossary());

            for (var i = 0; i < analysis.Result.Count; i++)
            {
                Assert.AreEqual(analysis.Result[i].Value, expectedNames[i]);
                Assert.AreEqual(analysis.Result[i].Type, expectedTypes[i]);
            }
        }
    }
}
