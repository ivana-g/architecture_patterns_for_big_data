# Email Verifier: Scientific Project Summary

## Abstract
The Email Verifier system is a distributed, message-driven application designed to provide robust, scalable, and high-throughput email verification as part of a user registration flow. It leverages microservices, asynchronous messaging, and persistent storage to ensure reliable and efficient processing of registration requests and email confirmations.

## Introduction
The intention of the Email Verifier application is to ensure that only valid email addresses are registered in a system by requiring users to confirm their email via a code. The system is architected to handle large volumes of requests, support horizontal scaling, and decouple registration from notification delivery using message queues.

## System Overview

### End-to-End Flow
1. **User Registration Request:**
   - User submits their email to the registration server via `/request-registration`.
2. **Registration Server:**
   - Stores the request in PostgreSQL.
   - Publishes a message to RabbitMQ.
3. **Notification Server:**
   - Listens to RabbitMQ for new registrations.
   - Sends a confirmation code via email (using a fake Sendgrid in development).
4. **User Confirms Registration:**
   - User submits the code to `/register`.
   - Registration server validates and confirms the registration.
5. **Fake Sendgrid:**
   - Simulates email delivery for development/testing.

### System Architecture
![System architecture](resources/system_architecture.png)

### User Flow Diagram
![User flow diagram](resources/user_flow_diagram.png)

## Methods (Technologies)

### Languages & Frameworks
- **Kotlin**: Main backend language (JVM)
- **Gradle**: Build system (Kotlin DSL)
- **JUnit**: Testing framework
- **Ktor**: Web server framework for Kotlin

### Libraries
- **Exposed**: Kotlin SQL library for database access
- **HikariCP**: JDBC connection pooling
- **RabbitMQ Java Client**: Messaging
- **Kotlinx Serialization**: JSON serialization
- **Logback**: Logging

### Infrastructure
- **PostgreSQL**: Relational database
- **RabbitMQ**: Message broker
- **Flyway**: (Optional, for DB migrations)
- **Sendgrid (Fake)**: Simulated email delivery

### APIs
- **REST APIs**: Exposed via Ktor servers for registration and notification
- **RabbitMQ Exchanges/Queues**: For inter-service communication

---

## System Architecture (Systems)

### A. Registration Server
- **Tech:** Ktor, Exposed, HikariCP, RabbitMQ client
- **Hooks Into:**
  - **PostgreSQL**: Reads/writes registration data
  - **RabbitMQ**: Publishes registration requests and notifications
- **Config Location:**
  - Environment variables (e.g., `DATABASE_URL`, `RABBIT_URL`)
  - Docker Compose for service wiring
  - See: `applications/registration-server/src/main/kotlin/io/initialcapacity/emailverifier/registrationserver/App.kt`

### B. Notification Server
- **Tech:** Ktor, Exposed, HikariCP, RabbitMQ client
- **Hooks Into:**
  - **PostgreSQL**: Reads/writes notification data
  - **RabbitMQ**: Consumes registration notifications
  - **Sendgrid (Fake)**: Sends emails via HTTP
- **Config Location:**
  - Environment variables (e.g., `DATABASE_URL`, `RABBIT_URL`, `SENDGRID_URL`, `SENDGRID_API_KEY`, `FROM_ADDRESS`)
  - Docker Compose for service wiring
  - See: `applications/notification-server/src/main/kotlin/io/initialcapacity/emailverifier/notificationserver/App.kt`

### C. Benchmark App
- **Tech:** Ktor client, custom benchmarking logic
- **Hooks Into:**
  - **Registration/Notification Servers**: Sends HTTP requests to simulate load
- **Config Location:**
  - Environment variables (e.g., `REGISTRATION_URL`, `REGISTRATION_COUNT`)
  - See: `applications/benchmark/src/main/kotlin/io/initialcapacity/emailverifier/benchmark/App.kt`

### D. RabbitMQ
- **Tech:** Docker Compose, RabbitMQ plugins
- **Hooks Into:**
  - **Registration/Notification Servers**: As message bus
- **Config Location:**
  - `docker-compose.yml` (service definition, volumes, plugins)
  - `configs` section for enabled plugins

### E. PostgreSQL
- **Tech:** Docker Compose, SQL init scripts
- **Hooks Into:**
  - **All servers**: As primary data store
- **Config Location:**
  - `docker-compose.yml` (service definition, volumes)
  - `databases/init-scripts/` (SQL for DB setup)

---

## Implementation Details (Code Mapping)

### A. Registration Server
- **App entry/config:**  
  `@path:applications/registration-server/src/main/kotlin/io/initialcapacity/emailverifier/registrationserver/App.kt`
  ```kotlin
  fun main(): Unit = runBlocking {
      val port = System.getenv("PORT")?.toInt() ?: 8081
      val rabbitUrl = System.getenv("RABBIT_URL")?.let(::URI)
      val databaseUrl = System.getenv("DATABASE_URL")
      val dbConfig = DatabaseConfiguration(databaseUrl)
      ...
  }
  ```
- **Database config:**  
  `@path:applications/registration-server/src/main/kotlin/io/initialcapacity/emailverifier/registrationserver/DatabaseConfiguration.kt`
  ```kotlin
  class DatabaseConfiguration(private val dbUrl: String) {
      private val config = HikariConfig().apply { jdbcUrl = dbUrl }
      private val ds = HikariDataSource(config)
      val db by lazy { Database.connect(ds) }
  }
  ```
- **RabbitMQ usage:**  
  `@path:applications/registration-server/src/main/kotlin/io/initialcapacity/emailverifier/registrationserver/App.kt`
  ```kotlin
  val connectionFactory = buildConnectionFactory(rabbitUrl)
  ...
  connectionFactory.declareAndBind(exchange = registrationNotificationExchange, queue = registrationNotificationQueue, routingKey = "42")
  ```

### B. Notification Server
- **App entry/config:**  
  `@path:applications/notification-server/src/main/kotlin/io/initialcapacity/emailverifier/notificationserver/App.kt`
  ```kotlin
  fun main() = runBlocking {
      val rabbitUrl = System.getenv("RABBIT_URL")?.let(::URI)
      val sendgridUrl = System.getenv("SENDGRID_URL")?.let { URI(it).toURL() }
      val databaseUrl = System.getenv("DATABASE_URL")
      ...
  }
  ```
- **Database config:**  
  `@path:applications/notification-server/src/main/kotlin/io/initialcapacity/emailverifier/notificationserver/DatabaseConfiguration.kt`
  ```kotlin
  class DatabaseConfiguration(private val dbUrl: String) {
      private val config = HikariConfig().apply { jdbcUrl = dbUrl }
      private val ds = HikariDataSource(config)
      val db by lazy { Database.connect(ds) }
  }
  ```
- **Sendgrid/Fake emailer config:**  
  `@path:applications/notification-server/src/main/kotlin/io/initialcapacity/emailverifier/notificationserver/App.kt`
  ```kotlin
  val sendgridUrl = System.getenv("SENDGRID_URL")?.let { URI(it).toURL() }
  val sendgridApiKey = System.getenv("SENDGRID_API_KEY")
  val fromAddress = System.getenv("FROM_ADDRESS")
  ```

### C. Benchmark App
- **Benchmark runner:**  
  `@path:applications/benchmark/src/main/kotlin/io/initialcapacity/emailverifier/benchmark/App.kt`
  ```kotlin
  fun main(): Unit = runBlocking {
      val port = getEnvInt("PORT", 9090)
      val benchmark = Benchmark(
          registrationUrl = System.getenv("REGISTRATION_URL") ?: "http://localhost:8081",
          registrationCount = getEnvInt("REGISTRATION_COUNT", 5_000),
          ...
      )
      ...
  }
  ```

### D. RabbitMQ & PostgreSQL (Docker Compose)
- **Service definitions:**  
  `@path:docker-compose.yml`
  ```yaml
  services:
    postgres-api:
      image: postgres:14.3
      ...
      volumes:
        - ./databases/init-scripts:/docker-entrypoint-initdb.d
        - pgdata:/var/lib/postgresql/data
    rabbitmq:
      image: rabbitmq:3.10.5-management
      ...
      configs:
        - source: plugins
          target: /etc/rabbitmq/enabled_plugins
      volumes:
        - rabbitmqdata:/var/lib/rabbitmq
        - rabbitmqlog:/var/log/rabbitmq
  ```
- **RabbitMQ plugin config:**  
  `@path:docker-compose.yml`
  ```yaml
  configs:
    plugins:
      content: "[rabbitmq_consistent_hash_exchange]."
  ```
- **Postgres init scripts:**  
  `@path:databases/init-scripts/` (directory for SQL files)

---

## Discussion

The Email Verifier system demonstrates a scalable, decoupled approach to email verification using microservices and asynchronous messaging. By leveraging RabbitMQ, the system can distribute load and scale horizontally, while PostgreSQL ensures data durability. The use of Docker Compose and fake services (like Sendgrid) enables easy local development and testing. The architecture is suitable for high-throughput environments and can be extended or modified for production use with real email providers and additional security or monitoring features.

--- 

## References

- [Ktor Documentation](https://ktor.io/docs/)
- [Exposed ORM Documentation](https://github.com/JetBrains/Exposed)
- [RabbitMQ Java Client](https://www.rabbitmq.com/java-client.html)
- [RabbitMQ Consistent Hash Exchange Plugin](https://github.com/rabbitmq/rabbitmq-server/tree/master/deps/rabbitmq_consistent_hash_exchange)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Sendgrid API Documentation](https://docs.sendgrid.com/for-developers/sending-email/api-getting-started)
- [Flyway Database Migrations](https://flywaydb.org/documentation/)
- [Kotlin Language](https://kotlinlang.org/)
- [Logback Logging](https://logback.qos.ch/) 