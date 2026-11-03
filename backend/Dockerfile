FROM eclipse-temurin:17-jdk AS build
WORKDIR /workspace

COPY . .
RUN chmod +x ./gradlew \
    && ./gradlew bootJar --no-daemon \
    && JAR="$(find build/libs -maxdepth 1 -type f -name '*.jar' ! -name '*-plain.jar' -print -quit)" \
    && test -n "$JAR" \
    && cp "$JAR" /app.jar

FROM eclipse-temurin:17-jre
RUN addgroup --system spring \
    && adduser --system --ingroup spring spring

WORKDIR /app
COPY --from=build --chown=spring:spring /app.jar app.jar

USER spring:spring
ENTRYPOINT ["java", "-jar", "/app/app.jar"]