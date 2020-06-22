package com.example.rtsLab31
import kotlin.math.*

fun factorize(n: Int): Pair<Int, Int> {
    var a = n
    var b = 1
    var x = ceil(sqrt(n.toDouble()))
    while (x < n){
        val t = x*x - n
        val y = truncate(sqrt(t))
        if (y * y == t) {
            a = (x - y).toInt()
            b = (x + y).toInt()
            break
        }
        x++
    }
    return Pair(a, b)
}

