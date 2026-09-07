package com.eosrmg.apps.materialui3

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.eosrmg.apps.materialui3.network.KtorClient
import com.eosrmg.apps.materialui3.network.LoginRequest
import com.eosrmg.apps.materialui3.network.LoginResponse
import com.eosrmg.apps.materialui3.network.NetworkResult
import com.eosrmg.apps.materialui3.network.User
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

class MainViewModel : ViewModel() {

    private val _usersState = MutableStateFlow<NetworkResult<List<User>>>(NetworkResult.Loading)
    val usersState = _usersState.asStateFlow()
    private val _loginState = MutableStateFlow<NetworkResult<LoginResponse>?>(null)
    val loginState = _loginState.asStateFlow()


    fun fetchUsers(){
        viewModelScope.launch{
            _usersState.value = NetworkResult.Loading
            val users = KtorClient.getUsers()
            if(users.isNotEmpty()){
                _usersState.value = NetworkResult.Success(users)
            }
            else{
                _usersState.value = NetworkResult.Error("Failed to fetch users")

            }

        }
    }

    fun login(username: String, password: String){
        viewModelScope.launch{
            _loginState.value = NetworkResult.Loading
            val result = KtorClient.login(LoginRequest(username, password))
            _loginState.value = result
            if (result is NetworkResult.Success){
                fetchUsers()

            }
        }
    }

    fun logout(){
        _loginState.value = null
        _usersState.value = NetworkResult.Loading
    }


}
