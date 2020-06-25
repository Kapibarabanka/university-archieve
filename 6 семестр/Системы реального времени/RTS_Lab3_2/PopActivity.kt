package com.example.rtsLab32

import android.support.v7.app.AppCompatActivity
import android.os.Bundle
import android.util.DisplayMetrics

import kotlinx.android.synthetic.main.activity_pop.*

class PopActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_pop)

        val dm = DisplayMetrics()
        windowManager.defaultDisplay.getMetrics(dm)

        val width: Int = (dm.widthPixels * 0.7).toInt()
        val height: Int = (dm.heightPixels* 0.1).toInt()

        window.setLayout(width, height)

        val duration = intent.getLongExtra("DURATION", 0)
        durationText.text = getString(R.string.trainingTime, (duration.toFloat() / 1000000000))
    }
}
