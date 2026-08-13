package com.eaos.aiide.ui

import android.os.Bundle
import android.view.View
import androidx.fragment.app.Fragment
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.WebSocket
import okhttp3.WebSocketListener

class ChatFragment : Fragment() {
    private var webSocket: WebSocket? = null

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        connectWebSocket()
    }

    private fun connectWebSocket() {
        val client = OkHttpClient()
        val request = Request.Builder().url("ws://10.0.2.2:8000/ws/chat").build()
        webSocket = client.newWebSocket(request, object : WebSocketListener() {
            override fun onOpen(webSocket: WebSocket, response: okhttp3.Response) {
                // Connected
            }
        })
    }
}