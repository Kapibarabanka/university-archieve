package com.example.rts_lab3_3

import android.os.Bundle
import android.support.v7.app.AppCompatActivity
import android.view.View
import android.widget.Toast
import kotlinx.android.synthetic.main.activity_main.*

class MainActivity : AppCompatActivity() {

    private var isSolved = false

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
    }

    fun onCalculateClick(view: View) {
        val coefs = listOf(a1.text.toString().toInt(),
            a2.text.toString().toInt(),
            a3.text.toString().toInt(),
            a4.text.toString().toInt())
        val answer = answerField.text.toString().toInt()
        var bestMutation = 1
        var (bestXs, bestDuration) = solve(coefs, answer, bestMutation / 10.0)
        for (i in 2..9) {
            val (xs, duration) = solve(coefs, answer, i / 10.0)
            if (isMoreOptimal(coefs, answer, xs, duration, bestDuration)) {
                bestXs = xs
                bestDuration = duration
                bestMutation = i * 10
            }
        }
        val toast = Toast.makeText(
            applicationContext,
            getString(R.string.solvingTime, bestDuration.first, bestDuration.second, bestMutation),
            Toast.LENGTH_LONG)
        toast.show()

        x1.setText(bestXs[0].toString())
        x2.setText(bestXs[1].toString())
        x3.setText(bestXs[2].toString())
        x4.setText(bestXs[3].toString())
    }

    private fun isMoreOptimal(coefs: List<Int>, answer: Int,
                              newXs: List<Int>, newDuration: Pair<Double, Int>,
                              bestDuration: Pair<Double, Int>): Boolean {
        if (!isSolved && calculateResult(coefs, newXs) == answer) {
            isSolved = true
            return true
        }

        return newDuration.second < bestDuration.second || newDuration.first < bestDuration.first
    }

}


