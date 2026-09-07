package com.eosrmg.apps.materialui3.ui

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.eosrmg.apps.materialui3.MainViewModel
import com.eosrmg.apps.materialui3.network.NetworkResult
import com.eosrmg.apps.materialui3.network.LoginResponse
import com.eosrmg.apps.materialui3.network.User

@Composable
fun NetworkingScreen(viewModel: MainViewModel = viewModel()) {
    val usersState by viewModel.usersState.collectAsState()
    val loginState by viewModel.loginState.collectAsState()

    var username by remember { mutableStateOf("emilys") }
    var password by remember { mutableStateOf("emilyspass") }
    var selectedUser by remember { mutableStateOf<User?>(null) }

    val isLoginIn = loginState is NetworkResult.Success


    Surface(
        modifier = Modifier.fillMaxSize(),
        color = MaterialTheme.colorScheme.background

    ){
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(16.dp),
            horizontalAlignment = Alignment.CenterHorizontally

        ){
            Text(
                text = "Ktor + Jetpack Compose",
                style = MaterialTheme.typography.headlineMedium,
                color = MaterialTheme.colorScheme.primary
            )
            Spacer(modifier = Modifier.height(16.dp))

            if(!isLoginIn){
                LoginForm(
                    username = username,
                    password = password,
                    onUsernameChange = {username = it},
                    onPasswordChange = {password = it},
                    loginState = loginState,
                ){
                    viewModel.login(username, password)

                }
            } else{
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween
                ){
                    Text(
                        "Welcome, ${(loginState as NetworkResult.Success).data.firstName}!",
                        style = MaterialTheme.typography.titleMedium,
                        color = MaterialTheme.colorScheme.primary

                    )
                    TextButton(onClick = {viewModel.logout()}){
                        Text("Logout")

                    }
                }
                Spacer(modifier = Modifier.height(16.dp))

                UsersList(state = usersState){
                    selectedUser = it
                }

            }

        }

    }

    selectedUser?.let { user ->
        UserDetailDialog(
            user = user,
            onDismiss = { selectedUser = null }
        )
    }
}

@Composable
fun UsersList(
    state: NetworkResult<List<User>>,
    onUserClick: (User) -> Unit,
) {
    when (state) {
        is NetworkResult.Loading -> {
            Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                CircularProgressIndicator()
            }
        }
        is NetworkResult.Success -> {
            LazyColumn(
                modifier = Modifier.fillMaxSize(),
                verticalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                items(state.data) { user ->
                    Card(
                        modifier = Modifier.fillMaxWidth(),
                        onClick = { onUserClick(user) },
                        colors = CardDefaults.cardColors(
                            containerColor = MaterialTheme.colorScheme.surfaceVariant
                        )
                    ) {
                        Column(modifier = Modifier.padding(16.dp)) {
                            Text(user.name, style = MaterialTheme.typography.titleMedium)
                            Text(user.email, style = MaterialTheme.typography.bodySmall)
                        }
                    }
                }
            }
        }
        is NetworkResult.Error -> {
            Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                Text("Error: ${state.message}", color = MaterialTheme.colorScheme.error)
            }
        }
    }
}

@Composable
fun UserDetailDialog(user: User, onDismiss: () -> Unit) {
    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text(user.name, style = MaterialTheme.typography.headlineSmall) },
        text = {
            Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
                DetailRow("Username", user.username)
                DetailRow("Email", user.email)
                DetailRow("Phone", user.phone)
                DetailRow("Website", user.website)
                HorizontalDivider()
                Text("Company", style = MaterialTheme.typography.labelLarge, color = MaterialTheme.colorScheme.primary)
                DetailRow("Name", user.company.name)
                DetailRow("Catchphrase", user.company.catchPhrase)
            }
        },
        confirmButton = {
            TextButton(onClick = onDismiss) {
                Text("Close")
            }
        }
    )
}

@Composable
fun DetailRow(label: String, value: String) {
    Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
        Text(label, style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.outline)
        Text(value, style = MaterialTheme.typography.bodyMedium)
    }
}

@Composable
fun LoginForm(
    username: String,
    password: String,
    onUsernameChange: (String) -> Unit,
    onPasswordChange: (String) -> Unit,
    loginState: NetworkResult<LoginResponse>?,
    onLoginClick: () -> Unit
) {
    Column(
        modifier = Modifier.fillMaxWidth(),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        OutlinedTextField(
            value = username,
            onValueChange = onUsernameChange,
            label = { Text("Username") },
            modifier = Modifier.fillMaxWidth()
        )
        Spacer(modifier = Modifier.height(8.dp))
        OutlinedTextField(
            value = password,
            onValueChange = onPasswordChange,
            label = { Text("Password") },
            modifier = Modifier.fillMaxWidth()
        )
        Spacer(modifier = Modifier.height(24.dp))
        Button(
            onClick = onLoginClick,
            modifier = Modifier.fillMaxWidth(),
            enabled = loginState !is NetworkResult.Loading
        ) {
            if (loginState is NetworkResult.Loading) {
                CircularProgressIndicator(
                    modifier = Modifier.size(24.dp),
                    color = MaterialTheme.colorScheme.onPrimary,
                    strokeWidth = 2.dp
                )
            } else {
                Text("Login")
            }
        }

        Spacer(modifier = Modifier.height(24.dp))

        when (loginState) {
            is NetworkResult.Success -> {
                Text(
                    "Success! Welcome ${loginState.data.firstName}",
                    color = MaterialTheme.colorScheme.primary,
                    style = MaterialTheme.typography.titleMedium
                )
            }
            is NetworkResult.Error -> {
                Text(
                    "Login Failed: ${loginState.message}",
                    color = MaterialTheme.colorScheme.error
                )
            }
            else -> {}
        }
    }
}
