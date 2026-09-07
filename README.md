# Modern Ktor Networking with Jetpack Compose 🚀

A professional, beginner-friendly Android application demonstrating modern networking using **Ktor**, **Jetpack Compose**, and **Clean Architecture**.

This project serves as the source code for the tutorial: **"Modern Android Networking with Ktor and Jetpack Compose for Beginners."**

---

## 📸 Preview

| Login Screen (POST) | User List (GET) | User Details (Dialog) |
|:---:|:---:|:---:|
| <img src="https://via.placeholder.com/200x400.png?text=Login+Screen" width="200" /> | <img src="https://via.placeholder.com/200x400.png?text=User+List" width="200" /> | <img src="https://via.placeholder.com/200x400.png?text=User+Details" width="200" /> |

---

## ✨ Features

- **Authentication (POST)**: Secure login flow using the [DummyJSON](https://dummyjson.com) API.
- **Data Fetching (GET)**: Dynamic user list retrieval from the [JSONPlaceholder](https://jsonplaceholder.typicode.com) API.
- **Clean Architecture**: Separation of concerns using **ViewModels**, **StateFlow**, and **Repository** patterns.
- **Modern UI**: Built entirely with **Jetpack Compose** and **Material 3**.
- **Custom Components**: Features the **BouncySwitch**—a high-quality, physics-based switch component.
- **Robust Networking**: Ktor 3.0 integration with JSON Serialization and logging.

---

## 🛠 Tech Stack

- **Language**: [Kotlin](https://kotlinlang.org/)
- **UI Framework**: [Jetpack Compose](https://developer.android.com/jetpack/compose)
- **Networking**: [Ktor Client](https://ktor.io/)
- **Serialization**: [Kotlinx Serialization](https://github.com/Kotlin/kotlinx.serialization)
- **Architecture**: MVVM (Model-View-ViewModel)
- **Asynchronous Flow**: [Kotlin Coroutines](https://kotlinlang.org/docs/coroutines-overview.html) & [StateFlow](https://kotlinlang.org/api/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines.flow/-state-flow/)

---

## 🚀 Getting Started

### Prerequisites
- Android Studio Ladybug (or newer)
- Android SDK 35+
- Internet connection (for API calls)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/eosrmg/Modern-Ktor-Networking.git
   ```
2. Open the project in Android Studio.
3. Sync Gradle and run the app on your emulator or physical device.

### Login Credentials
To test the login flow, use these [DummyJSON](https://dummyjson.com/docs/auth) credentials:
- **Username**: `emilys`
- **Password**: `emilyspass`

---

## 📖 What You'll Learn in the Tutorial

1. **Dependency Management**: Setting up Ktor using Version Catalogs (`libs.versions.toml`).
2. **The Ktor Client**: Building a singleton client with OkHttp and JSON plugins.
3. **Data Modeling**: Using `@Serializable` for nested JSON structures.
4. **ViewModel Logic**: Handling network states (`Loading`, `Success`, `Error`) reactively.
5. **State-Driven UI**: Building a Compose UI that reacts to authentication status.

---

## 🤝 Contributing
Feel free to fork this project and submit pull requests for any features or bug fixes!

## 📜 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
*Created by [eosrmg](https://github.com/eosrmg)*
