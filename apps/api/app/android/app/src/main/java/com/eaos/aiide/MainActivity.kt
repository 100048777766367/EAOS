package com.eaos.aiide

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import com.eaos.aiide.databinding.ActivityMainBinding

class MainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMainBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        binding.toolbarTitle.text = "⚡ EAOS Mobile IDE v6.0"
        binding.statusBadge.text = "Ready (100% Green)"
    }
}