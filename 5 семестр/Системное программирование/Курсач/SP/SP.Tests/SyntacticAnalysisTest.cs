using System;
using System.Collections.Generic;
using System.Linq;
using Microsoft.VisualStudio.TestTools.UnitTesting;

namespace SP.Tests
{
    [TestClass]
    public class SyntacticAnalysisTest
    {
        [TestMethod]
        public void MyVariantsTest()
        {
            var cExpression = "b=2*a[n]; b=d;";

            var c = new SyntacticAnalysis(cExpression, new Glossary());

            Assert.IsTrue(c.Errors.Count == 0);
        }

        [TestMethod]
        public void ExtraSpacesTest()
        {
            var cExpression = "b=2*a[n]; b d;";

            var c = new SyntacticAnalysis(cExpression, new Glossary());

            Assert.IsTrue(c.Errors.Any());
        }

        [TestMethod]
        public void BracketNotClosedTest()
        {
            var cExpression = "b=(2*a[n]; b = d;";

            var c = new SyntacticAnalysis(cExpression, new Glossary());

            Assert.IsTrue(c.Errors.Any());
        }

        [TestMethod]
        public void QuoteNotClosedTest()
        {
            {
                var cExpression = "b= \"fsdgdgd\";";

                var c = new SyntacticAnalysis(cExpression, new Glossary());

                Assert.IsTrue(c.Errors.Count == 0);
            }

            {
                var cExpression = "b= \"fsdgdgd;";

                var c = new SyntacticAnalysis(cExpression, new Glossary());

                Assert.IsTrue(c.Errors.Any());
            }
        }

        [TestMethod]
        public void BracketNotOpenedTest()
        {
            var cExpression = "b=2*a[n]); b = d;";

            var c = new SyntacticAnalysis(cExpression, new Glossary());

            Assert.IsTrue(c.Errors.Any());
        }

        [TestMethod]
        public void IndexerTest()
        {
            var cExpression = "b = a[];";

            var c = new SyntacticAnalysis(cExpression, new Glossary());

            Assert.IsTrue(c.Errors.Any());
        }

        [TestMethod]
        public void BinaryOperatorsNotWith2OperandsTest()
        {
            {
                var cExpression = "b = 1 + 3 * ;";

                var c = new SyntacticAnalysis(cExpression, new Glossary());

                Assert.IsTrue(c.Errors.Any());
            }

            {
                var cExpression = "b = 1 + /3 ;";

                var c = new SyntacticAnalysis(cExpression, new Glossary());

                Assert.IsTrue(c.Errors.Any());
            }
        }

        [TestMethod]
        public void AssignationTest()
        {
            var cExpression = "1 = 9;";

            var c = new SyntacticAnalysis(cExpression, new Glossary());

            Assert.IsTrue(c.Errors.Any());
        }

        [TestMethod]
        public void RandomTests()
        {
	        {
		        var cExpression = "a = (2* 3 + 0 - (1*7-(9+3)));";

		        var c = new SyntacticAnalysis(cExpression, new Glossary());

		        Assert.IsTrue(c.Errors.Count == 0);
			}
        }
	}
}
