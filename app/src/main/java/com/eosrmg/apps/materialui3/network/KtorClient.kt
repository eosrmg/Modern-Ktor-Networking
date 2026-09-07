package com.eosrmg.apps.materialui3.network

import io.ktor.client.HttpClient
import io.ktor.client.call.body
import io.ktor.client.engine.okhttp.OkHttp
import io.ktor.client.plugins.contentnegotiation.ContentNegotiation
import io.ktor.client.plugins.logging.LogLevel
import io.ktor.client.plugins.logging.Logging
import io.ktor.client.request.get
import io.ktor.client.request.post
import io.ktor.client.request.setBody
import io.ktor.client.utils.EmptyContent.contentType
import io.ktor.http.ContentType
import io.ktor.http.contentType
import io.ktor.serialization.kotlinx.json.json
import kotlinx.serialization.json.Json

object KtorClient {
    private val client = HttpClient(OkHttp){
        install(ContentNegotiation){
            json(Json{
                ignoreUnknownKeys = true
                prettyPrint = true
                isLenient = true
            })

        }
        install(Logging){
            level= LogLevel.ALL

        }

    }

    suspend fun getUsers(): List<User> {
        return try{
            client.get("https://jsonplaceholder.typicode.com/users").body()

        }
        catch (e: Exception){
            emptyList()

        }

    }

    suspend fun login(loginRequest: LoginRequest): NetworkResult<LoginResponse> {
        return try{
            val response: LoginResponse = client.post("https://dummyjson.com/auth/login"){
                contentType(ContentType.Application.Json)
                setBody(loginRequest)
            }.body()
            NetworkResult.Success(response)
        }
        catch (e: Exception){
            NetworkResult.Error(e.message ?: "Unknown error")

        }

    }
}











