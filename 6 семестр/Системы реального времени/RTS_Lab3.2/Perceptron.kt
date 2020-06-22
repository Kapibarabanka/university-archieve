package com.example.rtsLab32
import java.lang.System.nanoTime

class Perceptron(numberOfWeights: Int) {

    var weights: List<Double> = List(numberOfWeights) {0.0}

    fun train(data: List<Pair<List<Int>, Boolean>>, threshold: Int, speed: Double, isTimeDeadline: Boolean, deadline: Long): Pair<List<Boolean>, Long> {
        val innerDeadline: Long
        var counter: Long
        val count: () -> Unit
        val expectedClasses = (data.map{value -> value.second}).toList()
        var actualClasses = (expectedClasses.map{value -> !value}).toMutableList()
        if (isTimeDeadline) {
            count = {counter = nanoTime()}
            counter = nanoTime()
            innerDeadline =  counter + deadline
        }
        else {
            counter = 0
            count = {counter++}
            innerDeadline = deadline
        }
        val startTime = nanoTime()
        while (counter < innerDeadline) {
            for (i in 0 until data.count()) {
                val xs = data[i].first
                val output = weights.mapIndexed{idx, w -> w * xs[idx]}.sum()
                actualClasses[i] = getClass(output, threshold)
                if (trainIsEnded(expectedClasses, actualClasses)) return Pair(actualClasses, nanoTime() - startTime)
                val delta = threshold - output
                weights = weights.mapIndexed{idx, w -> w + delta * speed * xs[idx]}
            }
            count.invoke()
        }
        return Pair(actualClasses, nanoTime() - startTime)
    }

    private fun getClass(output: Double, threshold: Int): Boolean {return output > threshold}

    private fun trainIsEnded(expected: List<Boolean>, actual: List<Boolean>): Boolean {
        return expected.foldRightIndexed(true, {idx, exp, acc -> acc && (exp == actual[idx])})
    }
}
