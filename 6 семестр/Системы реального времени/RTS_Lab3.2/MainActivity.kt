package com.example.rtsLab32

import android.content.Intent
import android.databinding.DataBindingUtil
import android.support.v7.app.AppCompatActivity
import android.os.Bundle
import android.view.View
import android.widget.EditText
import android.widget.Spinner
import com.example.rtsLab32.databinding.ActivityMainBinding

import kotlinx.android.synthetic.main.activity_main.*
import kotlinx.android.synthetic.main.activity_pop.*
import kotlin.math.roundToLong

class MainActivity : AppCompatActivity() {

    private val perceptron: Perceptron = Perceptron(2)

    private lateinit var mainView: View

    private lateinit var pointsPrefixes: List<String>
    private lateinit var weightPrefix: String
    private lateinit var xSuffixes: List<String>
    private lateinit var expSuffix: String
    private lateinit var actSuffix: String

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val binding: ActivityMainBinding = DataBindingUtil.setContentView(
            this, R.layout.activity_main)
        mainView = findViewById(R.id.mainLayout)
        pointsPrefixes = resources.getStringArray(R.array.pointsPrefixes).toList()
        weightPrefix = resources.getString(R.string.weightPrefix)
        xSuffixes = listOf(resources.getString(R.string.X1), resources.getString(R.string.X2))
        expSuffix = resources.getString(R.string.Exp)
        actSuffix = resources.getString(R.string.Act)
    }

    fun onTrainClicked(view: View) {
        val data = pointsPrefixes.map { prefix -> getPoint(prefix, mainView) }
        val threshold = thresholdText.text.toString().toInt()
        val speed = speedSpinner.selectedItem.toString().toDouble()
        val isTimeDeadline = radioGroup2.checkedRadioButtonId == R.id.secondsButton
        val deadline = getDeadline(isTimeDeadline)

        val (actClasses, duration) = perceptron.train(data, threshold, speed, isTimeDeadline, deadline)

        pointsPrefixes.forEachIndexed{idx, prefix -> setFieldText(prefix, actSuffix, actClasses[idx].toString())}
        xSuffixes.forEachIndexed { idx, x -> setFieldText(weightPrefix, x, perceptron.weights[idx].toString()) }

        val intent = Intent(applicationContext, PopActivity::class.java)
        intent.putExtra("DURATION", duration)
        startActivity(intent)
    }

    fun onCleanClicked(view: View) {
        perceptron.weights = listOf(0.0, 0.0)
        xSuffixes.forEachIndexed { idx, x -> setFieldText(weightPrefix, x, perceptron.weights[idx].toString()) }
        pointsPrefixes.forEach{prefix -> setFieldText(prefix, actSuffix, "")}
    }

    private fun getFieldText(prefix: String, suffix: String): String {
        return mainView.findViewWithTag<EditText>("${prefix}${suffix}").text.toString()
    }

    private fun setFieldText(prefix: String, suffix: String, text: String) {
        mainView.findViewWithTag<EditText>("${prefix}${suffix}").setText(text)
    }

    private fun getPoint(prefix: String, mainView: View): Pair<List<Int>, Boolean> {
        val xs: List<Int> = xSuffixes.map{ getFieldText(prefix, it).toInt()}
        val expClass: Boolean = getFieldText(prefix, expSuffix) == "1"
        return Pair(xs, expClass)
    }

    private fun getDeadline(isTimeDeadline: Boolean): Long {
        return if (isTimeDeadline) {
            ((secondsSpinner.selectedItem.toString().toDouble() * 1000000000).roundToLong())
        } else {
            iterationsSpinner.selectedItem.toString().toLong()
        }
    }
}
