FROM maven:3.9.8-eclipse-temurin-17 AS build
WORKDIR /app
COPY pom.xml .
COPY src ./src
RUN mvn clean package -DskipTests

FROM eclipse-temurin:17-jre-jammy
ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app
RUN groupadd --system app && \
    useradd --system --gid app --home-dir /app --shell /usr/sbin/nologin app && \
    apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*
COPY --from=build /app/target/transaction-service-1.0.0.jar app.jar
RUN chown app:app /app/app.jar

USER app

HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
  CMD bash -c "exec 3<>/dev/tcp/127.0.0.1/8080 && printf 'GET /health HTTP/1.1\r\nHost: localhost\r\nConnection: close\r\n\r\n' >&3 && grep -q '200' <&3"

CMD ["java", "-jar", "app.jar"]
