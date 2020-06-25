package com.example.rts_lab3_3

import java.lang.System.nanoTime
import kotlin.math.abs
import kotlin.random.Random

const val populationSize = 20
const val maxIterations = 1000

fun solve(coefs: List<Int>, answer: Int, mutationProbability: Double): Pair<List<Int>, Pair<Double, Int>> {
    val startTime = nanoTime()
    var population = generatePopulation(coefs.count(), answer)
    var answers: List<Int> = listOf(0, 0, 0, 0)
    var iterations = 0
    while (true) {
        if (iterations++ > maxIterations)
            break
        val results = population.map { calculateResult(coefs, it) }
        val deltas = results.map { delta(answer, it) }
        var exit = false
        deltas.forEachIndexed { index, it ->
            if (it == 0) {
                answers = population[index]
                exit = true
            }
        }
        if (exit) break
        val possibilities = possibilities(deltas)
        val sectors = possibilities.mapIndexed { index, _ -> possibilities.take(index).sum() }
        val newPopulation = MutableList(population.count()) {population[it]}
        for (i in 0 until populationSize / 2) {
            val fatherChance = Random.nextDouble()
            val motherChance = Random.nextDouble()
            val fatherIndex = firstTrue(sectors) { x -> x >= fatherChance } - 1
            val motherIndex = firstTrue(sectors) { x -> x >= motherChance } - 1
            val father = population[fatherIndex]
            val mother = population[motherIndex]
            val threshold = Random.nextInt(0, populationSize - 1)
            val children = crossover(father, mother, threshold)
            newPopulation[i*2] = mutate(children.first, mutationProbability)
            newPopulation[i*2+1] = mutate(children.second, mutationProbability)
        }
        population = newPopulation
    }
    return answers to ((nanoTime() - startTime) / 1000000000.0 to iterations)
}

fun delta(expected: Int, actual: Int) = abs(expected - actual)

fun calculateResult(coefs: List<Int>, xs: List<Int>) = coefs.zip(xs) {a, x -> a * x}.sum()

fun possibilities(deltas: List<Int>): List<Double> {
    val sum = deltas.map { d -> 1.0 / d }.sum()
    return deltas.map { d -> 1.0 / d / sum }
}

fun crossover(d1: List<Int>, d2: List<Int>, border: Int): Pair<List<Int>, List<Int>> {
    val d1New = d1.mapIndexed{ index, it -> if (index <= border) it else d2[index] }
    val d2New = d2.mapIndexed{ index, it -> if (index <= border) it else d1[index] }
    return Pair(d1New, d2New)
}

fun mutate(d: List<Int>, mutationProbability: Double) =
    d.map{ if (Random.nextDouble() >= mutationProbability) it + Random.nextInt(-1, 1) else it }.toList()

fun generatePopulation(numberOfGenes: Int, answer: Int) : List<List<Int>> {
    val population = MutableList(populationSize) {List(numberOfGenes) {0} }
    for (i in 0 until populationSize) {
        population[i] = listOf(Random.nextInt(0, answer / 2),
            Random.nextInt(0, answer / 2),
            Random.nextInt(0, answer / 2),
            Random.nextInt(0, answer / 2))
    }
    return population
}

fun<T> firstTrue(d: List<T>, p: (T) -> Boolean): Int {
    for (i in d.indices) {
        if (p(d[i])) return i
    }
    return d.size - 1
}
