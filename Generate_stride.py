import os
from pathlib import Path

FILES = {
    ".github/workflows/build-apk.yml": """name: Build Stride APK

on:
  push:
    branches: [ "main", "master" ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up JDK 17
        uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'temurin'

      - name: Setup Android SDK
        uses: android-actions/setup-android@v3

      - name: Setup Gradle
        uses: gradle/actions/setup-gradle@v3
        with:
          gradle-version: '8.9'

      - name: Build Debug APK
        run: gradle assembleDebug --no-daemon

      - name: Upload APK Artifact
        uses: actions/upload-artifact@v4
        with:
          name: Stride-debug-apk
          path: app/build/outputs/apk/debug/app-debug.apk
""",

    "gradle/libs.versions.toml": """[versions]
agp = "8.7.2"
kotlin = "2.0.21"
ksp = "2.0.21-1.0.27"
coreKtx = "1.15.0"
lifecycle = "2.8.7"
activityCompose = "1.9.3"
composeBom = "2024.11.00"
navigationCompose = "2.8.4"
hilt = "2.52"
hiltNavigationCompose = "1.2.0"
hiltWork = "1.2.0"
room = "2.6.1"
datastore = "1.1.1"
work = "2.10.0"
playServicesLocation = "21.3.0"
playServicesMaps = "19.0.0"
mapsCompose = "6.2.1"
glance = "1.1.1"
coroutines = "1.9.0"
junit = "4.13.2"

[libraries]
androidx-core-ktx = { group = "androidx.core", name = "core-ktx", version.ref = "coreKtx" }
androidx-lifecycle-runtime-ktx = { group = "androidx.lifecycle", name = "lifecycle-runtime-ktx", version.ref = "lifecycle" }
androidx-lifecycle-runtime-compose = { group = "androidx.lifecycle", name = "lifecycle-runtime-compose", version.ref = "lifecycle" }
androidx-lifecycle-viewmodel-compose = { group = "androidx.lifecycle", name = "lifecycle-viewmodel-compose", version.ref = "lifecycle" }
androidx-activity-compose = { group = "androidx.activity", name = "activity-compose", version.ref = "activityCompose" }
androidx-compose-bom = { group = "androidx.compose", name = "compose-bom", version.ref = "composeBom" }
androidx-ui = { group = "androidx.compose.ui", name = "ui" }
androidx-ui-graphics = { group = "androidx.compose.ui", name = "ui-graphics" }
androidx-ui-tooling-preview = { group = "androidx.compose.ui", name = "ui-tooling-preview" }
androidx-material3 = { group = "androidx.compose.material3", name = "material3" }
androidx-material-icons-extended = { group = "androidx.compose.material", name = "material-icons-extended" }
androidx-navigation-compose = { group = "androidx.navigation", name = "navigation-compose", version.ref = "navigationCompose" }

hilt-android = { group = "com.google.dagger", name = "hilt-android", version.ref = "hilt" }
hilt-compiler = { group = "com.google.dagger", name = "hilt-android-compiler", version.ref = "hilt" }
androidx-hilt-navigation-compose = { group = "androidx.hilt", name = "hilt-navigation-compose", version.ref = "hiltNavigationCompose" }
androidx-hilt-work = { group = "androidx.hilt", name = "hilt-work", version.ref = "hiltWork" }
androidx-hilt-compiler = { group = "androidx.hilt", name = "hilt-compiler", version.ref = "hiltWork" }

room-runtime = { group = "androidx.room", name = "room-runtime", version.ref = "room" }
room-ktx = { group = "androidx.room", name = "room-ktx", version.ref = "room" }
room-compiler = { group = "androidx.room", name = "room-compiler", version.ref = "room" }

datastore-preferences = { group = "androidx.datastore", name = "datastore-preferences", version.ref = "datastore" }
work-runtime-ktx = { group = "androidx.work", name = "work-runtime-ktx", version.ref = "work" }

play-services-location = { group = "com.google.android.gms", name = "play-services-location", version.ref = "playServicesLocation" }
play-services-maps = { group = "com.google.android.gms", name = "play-services-maps", version.ref = "playServicesMaps" }
maps-compose = { group = "com.google.maps.android", name = "maps-compose", version.ref = "mapsCompose" }

glance-appwidget = { group = "androidx.glance", name = "glance-appwidget", version.ref = "glance" }
glance-material3 = { group = "androidx.glance", name = "glance-material3", version.ref = "glance" }

kotlinx-coroutines-android = { group = "org.jetbrains.kotlinx", name = "kotlinx-coroutines-android", version.ref = "coroutines" }
kotlinx-coroutines-play-services = { group = "org.jetbrains.kotlinx", name = "kotlinx-coroutines-play-services", version.ref = "coroutines" }
junit = { group = "junit", name = "junit", version.ref = "junit" }

[plugins]
android-application = { id = "com.android.application", version.ref = "agp" }
kotlin-android = { id = "org.jetbrains.kotlin.android", version.ref = "kotlin" }
kotlin-compose = { id = "org.jetbrains.kotlin.plugin.compose", version.ref = "kotlin" }
ksp = { id = "com.google.devtools.ksp", version.ref = "ksp" }
hilt = { id = "com.google.dagger.hilt.android", version.ref = "hilt" }
""",

    "settings.gradle.kts": """pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
}
rootProject.name = "Stride"
include(":app")
""",

    "build.gradle.kts": """plugins {
    alias(libs.plugins.android.application) apply false
    alias(libs.plugins.kotlin.android) apply false
    alias(libs.plugins.kotlin.compose) apply false
    alias(libs.plugins.ksp) apply false
    alias(libs.plugins.hilt) apply false
}
""",

    "gradle.properties": """org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
android.useAndroidX=true
kotlin.code.style=official
android.nonTransitiveRClass=true
""",

    "app/proguard-rules.pro": """# Keep Room entities and Hilt generated classes
-keep class com.stride.app.data.local.** { *; }
-dontwarn javax.annotation.**
""",

    "app/build.gradle.kts": """import java.util.Properties

plugins {
    alias(libs.plugins.android.application)
    alias(libs.plugins.kotlin.android)
    alias(libs.plugins.kotlin.compose)
    alias(libs.plugins.ksp)
    alias(libs.plugins.hilt)
}

val localProps = Properties().apply {
    val file = rootProject.file("local.properties")
    if (file.exists()) {
        file.inputStream().use { load(it) }
    }
}
val mapsApiKey: String = localProps.getProperty("MAPS_API_KEY", "")

android {
    namespace = "com.stride.app"
    compileSdk = 35

    defaultConfig {
        applicationId = "com.stride.app"
        minSdk = 26
        targetSdk = 35
        versionCode = 1
        versionName = "1.0.0"

        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
        manifestPlaceholders["MAPS_API_KEY"] = mapsApiKey
        buildConfigField("String", "MAPS_API_KEY", "\\"$mapsApiKey\\"")
    }

    buildTypes {
        release {
            isMinifyEnabled = true
            signingConfig = signingConfigs.getByName("debug")
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions {
        jvmTarget = "17"
    }
    buildFeatures {
        compose = true
        buildConfig = true
    }
}

dependencies {
    implementation(libs.androidx.core.ktx)
    implementation(libs.androidx.lifecycle.runtime.ktx)
    implementation(libs.androidx.lifecycle.runtime.compose)
    implementation(libs.androidx.lifecycle.viewmodel.compose)
    implementation(libs.androidx.activity.compose)

    implementation(platform(libs.androidx.compose.bom))
    implementation(libs.androidx.ui)
    implementation(libs.androidx.ui.graphics)
    implementation(libs.androidx.ui.tooling.preview)
    implementation(libs.androidx.material3)
    implementation(libs.androidx.material.icons.extended)
    implementation(libs.androidx.navigation.compose)

    implementation(libs.hilt.android)
    ksp(libs.hilt.compiler)
    implementation(libs.androidx.hilt.navigation.compose)
    implementation(libs.androidx.hilt.work)
    ksp(libs.androidx.hilt.compiler)

    implementation(libs.room.runtime)
    implementation(libs.room.ktx)
    ksp(libs.room.compiler)

    implementation(libs.datastore.preferences)
    implementation(libs.work.runtime.ktx)

    implementation(libs.play.services.location)
    implementation(libs.play.services.maps)
    implementation(libs.maps.compose)

    implementation(libs.glance.appwidget)
    implementation(libs.glance.material3)

    implementation(libs.kotlinx.coroutines.android)
    implementation(libs.kotlinx.coroutines.play.services)

    testImplementation(libs.junit)
}
""",

    "app/src/main/AndroidManifest.xml": """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools">

    <uses-permission android:name="android.permission.ACTIVITY_RECOGNITION" />
    <uses-permission android:name="com.google.android.gms.permission.ACTIVITY_RECOGNITION" />
    <uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />
    <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
    <uses-permission android:name="android.permission.ACCESS_BACKGROUND_LOCATION" />
    <uses-permission android:name="android.permission.POST_NOTIFICATIONS" />
    <uses-permission android:name="android.permission.FOREGROUND_SERVICE" />
    <uses-permission android:name="android.permission.FOREGROUND_SERVICE_HEALTH" />
    <uses-permission android:name="android.permission.FOREGROUND_SERVICE_LOCATION" />
    <uses-permission android:name="android.permission.RECEIVE_BOOT_COMPLETED" />
    <uses-permission android:name="android.permission.WAKE_LOCK" />

    <uses-feature
        android:name="android.hardware.sensor.stepcounter"
        android:required="false" />
    <uses-feature
        android:name="android.hardware.sensor.accelerometer"
        android:required="true" />
    <uses-feature
        android:name="android.hardware.location.gps"
        android:required="false" />

    <application
        android:name=".StrideApp"
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher"
        android:supportsRtl="true"
        android:theme="@style/Theme.Stride">

        <meta-data
            android:name="com.google.android.geo.API_KEY"
            android:value="${MAPS_API_KEY}" />

        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:screenOrientation="portrait"
            android:theme="@style/Theme.Stride"
            tools:ignore="LockedOrientationActivity">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>

        <service
            android:name=".service.TrackingService"
            android:enabled="true"
            android:exported="false"
            android:foregroundServiceType="health|location" />

        <receiver
            android:name=".service.BootReceiver"
            android:enabled="true"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.BOOT_COMPLETED" />
                <action android:name="android.intent.action.MY_PACKAGE_REPLACED" />
            </intent-filter>
        </receiver>

        <receiver
            android:name=".service.ActivityRecognitionReceiver"
            android:enabled="true"
            android:exported="false" />

        <receiver
            android:name=".widget.StrideWidgetReceiver"
            android:exported="true">
            <intent-filter>
                <action android:name="android.appwidget.action.APPWIDGET_UPDATE" />
            </intent-filter>
            <meta-data
                android:name="android.appwidget.provider"
                android:resource="@xml/stride_widget_info" />
        </receiver>

        <provider
            android:name="androidx.core.content.FileProvider"
            android:authorities="${applicationId}.fileprovider"
            android:exported="false"
            android:grantUriPermissions="true">
            <meta-data
                android:name="android.support.FILE_PROVIDER_PATHS"
                android:resource="@xml/file_paths" />
        </provider>

        <provider
            android:name="androidx.startup.InitializationProvider"
            android:authorities="${applicationId}.androidx-startup"
            android:exported="false"
            tools:node="merge">
            <meta-data
                android:name="androidx.work.WorkManagerInitializer"
                android:value="androidx.startup"
                tools:node="remove" />
        </provider>
    </application>
</manifest>
""",

    "app/src/main/res/values/strings.xml": """<resources>
    <string name="app_name">Stride</string>
    <string name="widget_description">Track your daily steps at a glance.</string>
</resources>
""",

    "app/src/main/res/values/themes.xml": """<resources>
    <style name="Theme.Stride" parent="android:Theme.Material.NoActionBar" />
</resources>
""",

    "app/src/main/res/xml/file_paths.xml": """<?xml version="1.0" encoding="utf-8"?>
<paths>
    <cache-path name="exports" path="exports/" />
</paths>
""",

    "app/src/main/res/xml/stride_widget_info.xml": """<?xml version="1.0" encoding="utf-8"?>
<appwidget-provider xmlns:android="http://schemas.android.com/apk/res/android"
    android:description="@string/widget_description"
    android:initialLayout="@layout/glance_default_loading_layout"
    android:minWidth="110dp"
    android:minHeight="110dp"
    android:resizeMode="horizontal|vertical"
    android:targetCellWidth="2"
    android:targetCellHeight="2"
    android:updatePeriodMillis="1800000"
    android:widgetCategory="home_screen" />
""",

    "app/src/main/res/drawable/ic_launcher_background.xml": """<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp"
    android:height="108dp"
    android:viewportWidth="108"
    android:viewportHeight="108">
    <path
        android:fillColor="#0E1110"
        android:pathData="M0,0h108v108h-108z" />
</vector>
""",

    "app/src/main/res/drawable/ic_launcher_foreground.xml": """<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp"
    android:height="108dp"
    android:viewportWidth="108"
    android:viewportHeight="108">
    <path
        android:fillColor="#00000000"
        android:pathData="M66,34 C66,27 42,27 42,39 C42,51 66,51 66,65 C66,77 42,77 42,70"
        android:strokeWidth="7"
        android:strokeColor="#0F9D7A"
        android:strokeLineCap="round" />
    <path
        android:fillColor="#0F9D7A"
        android:pathData="M66,34m-4,0a4,4 0,1 1,8 0a4,4 0,1 1,-8 0" />
</vector>
""",

    "app/src/main/res/mipmap-anydpi-v26/ic_launcher.xml": """<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@drawable/ic_launcher_background" />
    <foreground android:drawable="@drawable/ic_launcher_foreground" />
</adaptive-icon>
""",

    "app/src/main/java/com/stride/app/domain/model/Models.kt": """package com.stride.app.domain.model

enum class ActivityType(val label: String, val metMultiplier: Double) {
    WALK("Walk", 3.5),
    RUN("Run", 8.0),
    HIKE("Hike", 5.3)
}

enum class BiologicalSex { MALE, FEMALE, OTHER }
enum class UnitSystem { METRIC, IMPERIAL }
enum class AppTheme { SYSTEM, LIGHT, DARK }
enum class HistoryRange(val label: String) {
    DAY("Day"), WEEK("Week"), MONTH("Month"), YEAR("Year")
}

data class UserProfile(
    val heightCm: Int = 172,
    val weightKg: Float = 70f,
    val age: Int = 30,
    val sex: BiologicalSex = BiologicalSex.OTHER,
    val dailyGoal: Int = 10000,
    val unitSystem: UnitSystem = UnitSystem.METRIC,
    val theme: AppTheme = AppTheme.SYSTEM,
    val gpsEnabled: Boolean = true,
    val backgroundTrackingEnabled: Boolean = true,
    val calibratedStrideMeters: Double = 172 * 0.00415,
    val onboardingCompleted: Boolean = false
) {
    val defaultStrideMeters: Double
        get() = heightCm * 0.00415

    val effectiveStrideMeters: Double
        get() = if (calibratedStrideMeters in 0.4..1.35) calibratedStrideMeters else defaultStrideMeters
}

data class LatLngPoint(
    val latitude: Double,
    val longitude: Double,
    val timestampMs: Long = System.currentTimeMillis(),
    val speedMps: Float = 0f
)

data class DailySummary(
    val dateEpochDay: Long,
    val steps: Int,
    val goal: Int,
    val distanceMeters: Double,
    val caloriesKcal: Int,
    val activeMinutes: Int,
    val hourlySteps: List<Int> = List(24) { 0 }
)

data class ActivitySession(
    val id: Long = 0,
    val type: ActivityType,
    val startTimeMs: Long,
    val endTimeMs: Long,
    val durationSeconds: Long,
    val steps: Int,
    val distanceMeters: Double,
    val caloriesKcal: Int,
    val avgPaceSecPerKm: Int,
    val avgSpeedMps: Double,
    val avgCadenceSpm: Int,
    val routePoints: List<LatLngPoint>,
    val paceSplitsSecPerKm: List<Int>
)

data class LiveSessionState(
    val isActive: Boolean = false,
    val isPaused: Boolean = false,
    val type: ActivityType = ActivityType.WALK,
    val durationSeconds: Long = 0L,
    val steps: Int = 0,
    val distanceMeters: Double = 0.0,
    val currentPaceSecPerKm: Int = 0,
    val currentSpeedMps: Double = 0.0,
    val caloriesKcal: Int = 0,
    val cadenceSpm: Int = 0,
    val route: List<LatLngPoint> = emptyList(),
    val paceHistorySecPerKm: List<Int> = emptyList()
)

data class Badge(
    val id: String,
    val title: String,
    val description: String,
    val unlocked: Boolean
)

data class HistoryInsights(
    val averageSteps: Int,
    val bestDaySteps: Int,
    val currentStreakDays: Int,
    val totalDistanceKm: Double,
    val chartBars: List<Pair<String, Int>>,
    val badges: List<Badge>
)
""",

    "app/src/main/java/com/stride/app/domain/engine/StepFusionEngine.kt": """package com.stride.app.domain.engine

import com.stride.app.domain.model.LatLngPoint
import kotlin.math.atan2
import kotlin.math.cos
import kotlin.math.sin
import kotlin.math.sqrt

class StepFusionEngine(
    initialStrideLengthMeters: Double = 0.7138
) {
    companion object {
        const val MIN_STEP_INTERVAL_MS = 285L
        const val MAX_STEP_INTERVAL_MS = 1000L
        const val MAX_HUMAN_SPEED_MPS = 7.0f
        const val MAX_GPS_ACCURACY_METERS = 25.0f
        const val ACCEL_LOW_PASS_ALPHA = 0.2f
        const val ACCEL_PEAK_THRESHOLD = 11.4f
        const val MAX_GYRO_NOISE_RAD_S = 9.0f
    }

    var strideLengthMeters: Double = initialStrideLengthMeters.coerceIn(0.4, 1.35)
        private set

    var isInVehicle: Boolean = false
        private set
    var isStill: Boolean = false
        private set
    var currentGpsSpeedMps: Float = 0f
        private set

    private var lastRawHardwareSteps: Long? = null
    private var filteredAccelMag: Float = 9.81f
    private var previousAccelMag: Float = 9.81f
    private var isRising: Boolean = false
    private var lastValidatedStepTimeMs: Long = 0L
    private var recentGyroMagnitude: Float = 0.5f
    private val recentStepIntervalsMs = ArrayDeque<Long>(10)

    private var kalmanLat: Double? = null
    private var kalmanLng: Double? = null
    private var kalmanVariance: Double = -1.0
    private var lastGpsTimestampMs: Long = 0L

    private var calibrationGpsDistanceMeters: Double = 0.0
    private var calibrationValidatedSteps: Int = 0

    fun setActivityRecognitionState(inVehicle: Boolean, still: Boolean) {
        this.isInVehicle = inVehicle
        this.isStill = still
    }

    fun processHardwareStepCounter(rawSteps: Long, timestampMs: Long): Int {
        val previous = lastRawHardwareSteps
        if (previous == null) {
            lastRawHardwareSteps = rawSteps
            return 0
        }

        val rawDelta = if (rawSteps < previous) {
            rawSteps.toInt().coerceAtLeast(0)
        } else {
            (rawSteps - previous).toInt()
        }
        lastRawHardwareSteps = rawSteps

        if (rawDelta <= 0) return 0
        if (isRejectedByEnvironment()) return 0

        if (lastValidatedStepTimeMs > 0L && rawDelta == 1) {
            val interval = timestampMs - lastValidatedStepTimeMs
            if (interval in 1 until MIN_STEP_INTERVAL_MS) {
                return 0
            }
            recordStepInterval(interval)
        }
        lastValidatedStepTimeMs = timestampMs
        return rawDelta.coerceAtMost(500)
    }

    fun processGyroscope(gx: Float, gy: Float, gz: Float) {
        val mag = sqrt(gx * gx + gy * gy + gz * gz)
        recentGyroMagnitude = 0.3f * mag + 0.7f * recentGyroMagnitude
    }

    fun processAccelerometer(ax: Float, ay: Float, az: Float, timestampMs: Long): Int {
        if (isRejectedByEnvironment()) return 0

        val rawMag = sqrt(ax * ax + ay * ay + az * az)
        filteredAccelMag = ACCEL_LOW_PASS_ALPHA * rawMag + (1f - ACCEL_LOW_PASS_ALPHA) * filteredAccelMag

        var stepDetected = 0
        if (filteredAccelMag > previousAccelMag) {
            isRising = true
        } else if (isRising && previousAccelMag >= ACCEL_PEAK_THRESHOLD) {
            isRising = false
            val interval = timestampMs - lastValidatedStepTimeMs

            val cadenceValid = if (lastValidatedStepTimeMs == 0L) {
                true
            } else {
                interval in MIN_STEP_INTERVAL_MS..MAX_STEP_INTERVAL_MS ||
                    (interval > MAX_STEP_INTERVAL_MS && interval < 5000L)
            }

            val gyroValid = recentGyroMagnitude <= MAX_GYRO_NOISE_RAD_S

            if (cadenceValid && gyroValid && interval >= MIN_STEP_INTERVAL_MS) {
                if (lastValidatedStepTimeMs > 0L && interval <= MAX_STEP_INTERVAL_MS) {
                    recordStepInterval(interval)
                }
                lastValidatedStepTimeMs = timestampMs
                stepDetected = 1
            }
        }
        previousAccelMag = filteredAccelMag
        return stepDetected
    }

    fun processGpsLocation(
        lat: Double,
        lng: Double,
        accuracyMeters: Float,
        speedMps: Float,
        timestampMs: Long,
        stepsSinceLastFix: Int = 0
    ): GpsFusionResult {
        currentGpsSpeedMps = speedMps

        if (accuracyMeters > MAX_GPS_ACCURACY_METERS || accuracyMeters <= 0f) {
            return GpsFusionResult(accepted = false, deltaDistanceMeters = 0.0, smoothedPoint = null)
        }

        val prevLat = kalmanLat
        val prevLng = kalmanLng

        if (prevLat == null || prevLng == null || kalmanVariance < 0) {
            kalmanLat = lat
            kalmanLng = lng
            kalmanVariance = (accuracyMeters * accuracyMeters).toDouble()
            lastGpsTimestampMs = timestampMs
            return GpsFusionResult(
                accepted = true,
                deltaDistanceMeters = 0.0,
                smoothedPoint = LatLngPoint(lat, lng, timestampMs, speedMps)
            )
        }

        val dtSeconds = ((timestampMs - lastGpsTimestampMs).coerceAtLeast(1L)) / 1000.0
        val rawDistance = haversineMeters(prevLat, prevLng, lat, lng)
        val impliedSpeed = rawDistance / dtSeconds

        if (impliedSpeed > 11.0) {
            return GpsFusionResult(accepted = false, deltaDistanceMeters = 0.0, smoothedPoint = null)
        }

        val processNoiseMps = 3.0
        kalmanVariance += dtSeconds * processNoiseMps * processNoiseMps
        val measurementVariance = (accuracyMeters * accuracyMeters).toDouble()
        val kalmanGain = kalmanVariance / (kalmanVariance + measurementVariance)

        val smoothedLat = prevLat + kalmanGain * (lat - prevLat)
        val smoothedLng = prevLng + kalmanGain * (lng - prevLng)
        kalmanVariance = (1.0 - kalmanGain) * kalmanVariance
        lastGpsTimestampMs = timestampMs

        val smoothedDelta = haversineMeters(prevLat, prevLng, smoothedLat, smoothedLng)
        kalmanLat = smoothedLat
        kalmanLng = smoothedLng

        val effectiveDelta = if (smoothedDelta < 0.8 && speedMps < 0.4f) 0.0 else smoothedDelta

        if (effectiveDelta > 1.5 && stepsSinceLastFix > 2 && speedMps in 0.7f..6.5f) {
            calibrationGpsDistanceMeters += effectiveDelta
            calibrationValidatedSteps += stepsSinceLastFix
            if (calibrationValidatedSteps >= 40) {
                val measuredStride = calibrationGpsDistanceMeters / calibrationValidatedSteps
                if (measuredStride in 0.45..1.30) {
                    strideLengthMeters = (0.8 * strideLengthMeters + 0.2 * measuredStride).coerceIn(0.45, 1.30)
                }
            }
        }

        return GpsFusionResult(
            accepted = true,
            deltaDistanceMeters = effectiveDelta,
            smoothedPoint = LatLngPoint(smoothedLat, smoothedLng, timestampMs, speedMps)
        )
    }

    fun getCurrentCadenceSpm(nowMs: Long = lastValidatedStepTimeMs): Int {
        if (recentStepIntervalsMs.isEmpty()) return 0
        if (nowMs - lastValidatedStepTimeMs > 4000L) return 0
        val avgIntervalMs = recentStepIntervalsMs.average()
        if (avgIntervalMs <= 0.0) return 0
        return (60_000.0 / avgIntervalMs).toInt().coerceIn(0, 220)
    }

    fun estimateDistanceMeters(steps: Int): Double = steps * strideLengthMeters

    fun resetSessionGpsState() {
        kalmanLat = null
        kalmanLng = null
        kalmanVariance = -1.0
        lastGpsTimestampMs = 0L
        currentGpsSpeedMps = 0f
        calibrationGpsDistanceMeters = 0.0
        calibrationValidatedSteps = 0
    }

    private fun isRejectedByEnvironment(): Boolean {
        if (isInVehicle) return true
        if (currentGpsSpeedMps > MAX_HUMAN_SPEED_MPS) return true
        return false
    }

    private fun recordStepInterval(intervalMs: Long) {
        if (intervalMs in MIN_STEP_INTERVAL_MS..MAX_STEP_INTERVAL_MS) {
            if (recentStepIntervalsMs.size >= 8) {
                recentStepIntervalsMs.removeFirst()
            }
            recentStepIntervalsMs.addLast(intervalMs)
        }
    }

    fun haversineMeters(lat1: Double, lon1: Double, lat2: Double, lon2: Double): Double {
        val r = 6371000.0
        val dLat = Math.toRadians(lat2 - lat1)
        val dLon = Math.toRadians(lon2 - lon1)
        val a = sin(dLat / 2) * sin(dLat / 2) +
            cos(Math.toRadians(lat1)) * cos(Math.toRadians(lat2)) *
            sin(dLon / 2) * sin(dLon / 2)
        val c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return r * c
    }

    data class GpsFusionResult(
        val accepted: Boolean,
        val deltaDistanceMeters: Double,
        val smoothedPoint: LatLngPoint?
    )
}
""",

    "app/src/main/java/com/stride/app/domain/engine/DayRolloverCalculator.kt": """package com.stride.app.domain.engine

object DayRolloverCalculator {

    data class CounterSnapshot(
        val dateEpochDay: Long,
        val savedStepsToday: Int,
        val lastHardwareReading: Long
    )

    data class ReconciliationResult(
        val dateEpochDay: Long,
        val updatedStepsToday: Int,
        val deltaAdded: Int,
        val newHardwareBaseline: Long,
        val isNewDay: Boolean
    )

    fun reconcile(
        snapshot: CounterSnapshot?,
        currentEpochDay: Long,
        currentHardwareSteps: Long
    ): ReconciliationResult {
        if (snapshot == null) {
            return ReconciliationResult(
                dateEpochDay = currentEpochDay,
                updatedStepsToday = 0,
                deltaAdded = 0,
                newHardwareBaseline = currentHardwareSteps,
                isNewDay = true
            )
        }

        if (currentEpochDay > snapshot.dateEpochDay) {
            return ReconciliationResult(
                dateEpochDay = currentEpochDay,
                updatedStepsToday = 0,
                deltaAdded = 0,
                newHardwareBaseline = currentHardwareSteps,
                isNewDay = true
            )
        }

        val delta = if (currentHardwareSteps < snapshot.lastHardwareReading) {
            currentHardwareSteps.toInt().coerceAtLeast(0)
        } else {
            (currentHardwareSteps - snapshot.lastHardwareReading).toInt()
        }

        val updatedSteps = snapshot.savedStepsToday + delta
        return ReconciliationResult(
            dateEpochDay = currentEpochDay,
            updatedStepsToday = updatedSteps,
            deltaAdded = delta,
            newHardwareBaseline = currentHardwareSteps,
            isNewDay = false
        )
    }
}
""",

    "app/src/main/java/com/stride/app/domain/usecase/CalculateStatsUseCase.kt": """package com.stride.app.domain.usecase

import com.stride.app.domain.model.ActivitySession
import com.stride.app.domain.model.ActivityType
import com.stride.app.domain.model.Badge
import com.stride.app.domain.model.DailySummary
import com.stride.app.domain.model.HistoryInsights
import com.stride.app.domain.model.UserProfile
import javax.inject.Inject
import kotlin.math.roundToInt

class CalculateStatsUseCase @Inject constructor() {

    fun estimateCaloriesFromSteps(steps: Int, profile: UserProfile): Int {
        val weightFactor = profile.weightKg / 70.0
        val strideFactor = profile.effectiveStrideMeters / 0.715
        return (steps * 0.04 * weightFactor * strideFactor).roundToInt()
    }

    fun estimateSessionCalories(
        type: ActivityType,
        durationSeconds: Long,
        weightKg: Float
    ): Int {
        val hours = durationSeconds / 3600.0
        return (type.metMultiplier * weightKg * hours).roundToInt().coerceAtLeast(0)
    }

    fun estimateActiveMinutes(steps: Int): Int = (steps / 100).coerceAtLeast(0)

    fun buildInsights(
        days: List<DailySummary>,
        sessions: List<ActivitySession>,
        chartBars: List<Pair<String, Int>>,
        todayEpochDay: Long
    ): HistoryInsights {
        val nonEmptyDays = days.filter { it.steps > 0 }
        val avgSteps = if (nonEmptyDays.isNotEmpty()) {
            nonEmptyDays.map { it.steps }.average().roundToInt()
        } else 0

        val bestDay = days.maxOfOrNull { it.steps } ?: 0
        val totalDistanceKm = days.sumOf { it.distanceMeters } / 1000.0

        val byDay = days.associateBy { it.dateEpochDay }
        var streak = 0
        var cursor = todayEpochDay
        val todayRec = byDay[cursor]
        if (todayRec == null || todayRec.steps < todayRec.goal) {
            cursor -= 1
        }
        while (true) {
            val d = byDay[cursor]
            if (d != null && d.steps >= d.goal) {
                streak++
                cursor--
            } else {
                break
            }
        }

        val badges = listOf(
            Badge(
                id = "first_5k",
                title = "First 5K",
                description = "Walk 5,000 steps in a single day",
                unlocked = bestDay >= 5000
            ),
            Badge(
                id = "10k_day",
                title = "10K Club",
                description = "Reach 10,000 steps in a single day",
                unlocked = bestDay >= 10000
            ),
            Badge(
                id = "streak_7",
                title = "7-Day Streak",
                description = "Hit your daily goal 7 days in a row",
                unlocked = streak >= 7 || hasHistoricalSevenDayStreak(days)
            ),
            Badge(
                id = "total_100km",
                title = "100 km Milestone",
                description = "Cover 100 kilometers of total distance",
                unlocked = totalDistanceKm >= 100.0 || sessions.sumOf { it.distanceMeters } >= 100_000.0
            )
        )

        return HistoryInsights(
            averageSteps = avgSteps,
            bestDaySteps = bestDay,
            currentStreakDays = streak,
            totalDistanceKm = totalDistanceKm,
            chartBars = chartBars,
            badges = badges
        )
    }

    private fun hasHistoricalSevenDayStreak(days: List<DailySummary>): Boolean {
        val sorted = days.sortedBy { it.dateEpochDay }
        var current = 0
        var lastDay = Long.MIN_VALUE
        for (d in sorted) {
            if (d.steps >= d.goal) {
                current = if (d.dateEpochDay == lastDay + 1) current + 1 else 1
                lastDay = d.dateEpochDay
                if (current >= 7) return true
            } else {
                current = 0
            }
        }
        return false
    }
}
""",

    "app/src/main/java/com/stride/app/domain/usecase/ExportCsvUseCase.kt": """package com.stride.app.domain.usecase

import android.content.Context
import android.net.Uri
import androidx.core.content.FileProvider
import com.stride.app.domain.model.ActivitySession
import com.stride.app.domain.model.DailySummary
import dagger.hilt.android.qualifiers.ApplicationContext
import java.io.File
import java.time.LocalDate
import javax.inject.Inject

class ExportCsvUseCase @Inject constructor(
    @ApplicationContext private val context: Context
) {
    fun exportToCsvUri(days: List<DailySummary>, sessions: List<ActivitySession>): Uri {
        val exportDir = File(context.cacheDir, "exports").apply { mkdirs() }
        val file = File(exportDir, "stride_export_${System.currentTimeMillis()}.csv")

        val sb = StringBuilder()
        sb.appendLine("# DAILY STEPS")
        sb.appendLine("Date,Steps,Goal,Distance_Meters,Calories_Kcal,Active_Minutes")
        days.sortedByDescending { it.dateEpochDay }.forEach { day ->
            val dateStr = LocalDate.ofEpochDay(day.dateEpochDay).toString()
            sb.appendLine("$dateStr,${day.steps},${day.goal},${"%.1f".format(day.distanceMeters)},${day.caloriesKcal},${day.activeMinutes}")
        }

        sb.appendLine()
        sb.appendLine("# ACTIVITY SESSIONS")
        sb.appendLine("ID,Type,Start_Timestamp_Ms,Duration_Sec,Steps,Distance_Meters,Calories_Kcal,Avg_Pace_Sec_Km")
        sessions.sortedByDescending { it.startTimeMs }.forEach { s ->
            sb.appendLine("${s.id},${s.type.name},${s.startTimeMs},${s.durationSeconds},${s.steps},${"%.1f".format(s.distanceMeters)},${s.caloriesKcal},${s.avgPaceSecPerKm}")
        }

        file.writeText(sb.toString())
        return FileProvider.getUriForFile(
            context,
            "${context.packageName}.fileprovider",
            file
        )
    }
}
""",

    "app/src/main/java/com/stride/app/data/local/Entities.kt": """package com.stride.app.data.local

import androidx.room.Entity
import androidx.room.PrimaryKey
import com.stride.app.domain.model.ActivitySession
import com.stride.app.domain.model.ActivityType
import com.stride.app.domain.model.DailySummary
import com.stride.app.domain.model.LatLngPoint

@Entity(tableName = "daily_steps")
data class DailyStepEntity(
    @PrimaryKey val dateEpochDay: Long,
    val steps: Int,
    val goal: Int,
    val distanceMeters: Double,
    val caloriesKcal: Int,
    val activeMinutes: Int,
    val lastHardwareCounter: Long,
    val hourlyStepsCsv: String,
    val goalNotified: Boolean = false
) {
    fun toDomain(): DailySummary {
        val hourly = hourlyStepsCsv.split(",")
            .mapNotNull { it.trim().toIntOrNull() }
            .let { list -> if (list.size == 24) list else List(24) { idx -> list.getOrElse(idx) { 0 } } }
        return DailySummary(
            dateEpochDay = dateEpochDay,
            steps = steps,
            goal = goal,
            distanceMeters = distanceMeters,
            caloriesKcal = caloriesKcal,
            activeMinutes = activeMinutes,
            hourlySteps = hourly
        )
    }
}

@Entity(tableName = "activity_sessions")
data class ActivitySessionEntity(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val type: String,
    val startTimeMs: Long,
    val endTimeMs: Long,
    val durationSeconds: Long,
    val steps: Int,
    val distanceMeters: Double,
    val caloriesKcal: Int,
    val avgPaceSecPerKm: Int,
    val avgSpeedMps: Double,
    val avgCadenceSpm: Int,
    val encodedRoute: String,
    val paceSplitsCsv: String
) {
    fun toDomain(): ActivitySession {
        val points = if (encodedRoute.isBlank()) emptyList() else {
            encodedRoute.split(";").mapNotNull { token ->
                val parts = token.split(",")
                if (parts.size >= 2) {
                    val lat = parts[0].toDoubleOrNull() ?: return@mapNotNull null
                    val lng = parts[1].toDoubleOrNull() ?: return@mapNotNull null
                    val ts = parts.getOrNull(2)?.toLongOrNull() ?: 0L
                    val spd = parts.getOrNull(3)?.toFloatOrNull() ?: 0f
                    LatLngPoint(lat, lng, ts, spd)
                } else null
            }
        }
        val splits = if (paceSplitsCsv.isBlank()) emptyList() else {
            paceSplitsCsv.split(",").mapNotNull { it.trim().toIntOrNull() }
        }
        return ActivitySession(
            id = id,
            type = runCatching { ActivityType.valueOf(type) }.getOrDefault(ActivityType.WALK),
            startTimeMs = startTimeMs,
            endTimeMs = endTimeMs,
            durationSeconds = durationSeconds,
            steps = steps,
            distanceMeters = distanceMeters,
            caloriesKcal = caloriesKcal,
            avgPaceSecPerKm = avgPaceSecPerKm,
            avgSpeedMps = avgSpeedMps,
            avgCadenceSpm = avgCadenceSpm,
            routePoints = points,
            paceSplitsSecPerKm = splits
        )
    }

    companion object {
        fun fromDomain(session: ActivitySession): ActivitySessionEntity {
            val encoded = session.routePoints.joinToString(";") {
                "${it.latitude},${it.longitude},${it.timestampMs},${it.speedMps}"
            }
            val splits = session.paceSplitsSecPerKm.joinToString(",")
            return ActivitySessionEntity(
                id = session.id,
                type = session.type.name,
                startTimeMs = session.startTimeMs,
                endTimeMs = session.endTimeMs,
                durationSeconds = session.durationSeconds,
                steps = session.steps,
                distanceMeters = session.distanceMeters,
                caloriesKcal = session.caloriesKcal,
                avgPaceSecPerKm = session.avgPaceSecPerKm,
                avgSpeedMps = session.avgSpeedMps,
                avgCadenceSpm = session.avgCadenceSpm,
                encodedRoute = encoded,
                paceSplitsCsv = splits
            )
        }
    }
}
""",

    "app/src/main/java/com/stride/app/data/local/StrideDao.kt": """package com.stride.app.data.local

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import kotlinx.coroutines.flow.Flow

@Dao
interface StrideDao {

    @Query("SELECT * FROM daily_steps WHERE dateEpochDay = :epochDay LIMIT 1")
    fun observeDay(epochDay: Long): Flow<DailyStepEntity?>

    @Query("SELECT * FROM daily_steps WHERE dateEpochDay = :epochDay LIMIT 1")
    suspend fun getDay(epochDay: Long): DailyStepEntity?

    @Query("SELECT * FROM daily_steps ORDER BY dateEpochDay DESC")
    fun observeAllDays(): Flow<List<DailyStepEntity>>

    @Query("SELECT * FROM daily_steps ORDER BY dateEpochDay DESC")
    suspend fun getAllDays(): List<DailyStepEntity>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun upsertDay(entity: DailyStepEntity)

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertSession(entity: ActivitySessionEntity): Long

    @Query("SELECT * FROM activity_sessions ORDER BY startTimeMs DESC")
    fun observeAllSessions(): Flow<List<ActivitySessionEntity>>

    @Query("SELECT * FROM activity_sessions ORDER BY startTimeMs DESC")
    suspend fun getAllSessions(): List<ActivitySessionEntity>

    @Query("SELECT * FROM activity_sessions WHERE id = :id LIMIT 1")
    suspend fun getSessionById(id: Long): ActivitySessionEntity?

    @Query("DELETE FROM daily_steps")
    suspend fun deleteAllDays()

    @Query("DELETE FROM activity_sessions")
    suspend fun deleteAllSessions()
}
""",

    "app/src/main/java/com/stride/app/data/local/StrideDatabase.kt": """package com.stride.app.data.local

import androidx.room.Database
import androidx.room.RoomDatabase

@Database(
    entities = [DailyStepEntity::class, ActivitySessionEntity::class],
    version = 1,
    exportSchema = false
)
abstract class StrideDatabase : RoomDatabase() {
    abstract fun strideDao(): StrideDao
}
""",

    "app/src/main/java/com/stride/app/data/datastore/UserPreferencesRepository.kt": """package com.stride.app.data.datastore

import android.content.Context
import androidx.datastore.preferences.core.booleanPreferencesKey
import androidx.datastore.preferences.core.doublePreferencesKey
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.core.floatPreferencesKey
import androidx.datastore.preferences.core.intPreferencesKey
import androidx.datastore.preferences.core.stringPreferencesKey
import androidx.datastore.preferences.preferencesDataStore
import com.stride.app.domain.model.AppTheme
import com.stride.app.domain.model.BiologicalSex
import com.stride.app.domain.model.UnitSystem
import com.stride.app.domain.model.UserProfile
import dagger.hilt.android.qualifiers.ApplicationContext
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map
import javax.inject.Inject
import javax.inject.Singleton

private val Context.dataStore by preferencesDataStore(name = "stride_preferences")

@Singleton
class UserPreferencesRepository @Inject constructor(
    @ApplicationContext private val context: Context
) {
    private object Keys {
        val HEIGHT_CM = intPreferencesKey("height_cm")
        val WEIGHT_KG = floatPreferencesKey("weight_kg")
        val AGE = intPreferencesKey("age")
        val SEX = stringPreferencesKey("sex")
        val DAILY_GOAL = intPreferencesKey("daily_goal")
        val UNIT_SYSTEM = stringPreferencesKey("unit_system")
        val THEME = stringPreferencesKey("theme")
        val GPS_ENABLED = booleanPreferencesKey("gps_enabled")
        val BG_TRACKING = booleanPreferencesKey("bg_tracking")
        val CALIBRATED_STRIDE = doublePreferencesKey("calibrated_stride")
        val ONBOARDING_DONE = booleanPreferencesKey("onboarding_done")
    }

    val userProfileFlow: Flow<UserProfile> = context.dataStore.data.map { prefs ->
        val height = prefs[Keys.HEIGHT_CM] ?: 172
        UserProfile(
            heightCm = height,
            weightKg = prefs[Keys.WEIGHT_KG] ?: 70f,
            age = prefs[Keys.AGE] ?: 30,
            sex = prefs[Keys.SEX]?.let { runCatching { BiologicalSex.valueOf(it) }.getOrNull() }
                ?: BiologicalSex.OTHER,
            dailyGoal = prefs[Keys.DAILY_GOAL] ?: 10000,
            unitSystem = prefs[Keys.UNIT_SYSTEM]?.let { runCatching { UnitSystem.valueOf(it) }.getOrNull() }
                ?: UnitSystem.METRIC,
            theme = prefs[Keys.THEME]?.let { runCatching { AppTheme.valueOf(it) }.getOrNull() }
                ?: AppTheme.SYSTEM,
            gpsEnabled = prefs[Keys.GPS_ENABLED] ?: true,
            backgroundTrackingEnabled = prefs[Keys.BG_TRACKING] ?: true,
            calibratedStrideMeters = prefs[Keys.CALIBRATED_STRIDE] ?: (height * 0.00415),
            onboardingCompleted = prefs[Keys.ONBOARDING_DONE] ?: false
        )
    }

    suspend fun updateProfile(transform: (UserProfile) -> UserProfile) {
        context.dataStore.edit { prefs ->
            val currentHeight = prefs[Keys.HEIGHT_CM] ?: 172
            val current = UserProfile(
                heightCm = currentHeight,
                weightKg = prefs[Keys.WEIGHT_KG] ?: 70f,
                age = prefs[Keys.AGE] ?: 30,
                sex = prefs[Keys.SEX]?.let { runCatching { BiologicalSex.valueOf(it) }.getOrNull() }
                    ?: BiologicalSex.OTHER,
                dailyGoal = prefs[Keys.DAILY_GOAL] ?: 10000,
                unitSystem = prefs[Keys.UNIT_SYSTEM]?.let { runCatching { UnitSystem.valueOf(it) }.getOrNull() }
                    ?: UnitSystem.METRIC,
                theme = prefs[Keys.THEME]?.let { runCatching { AppTheme.valueOf(it) }.getOrNull() }
                    ?: AppTheme.SYSTEM,
                gpsEnabled = prefs[Keys.GPS_ENABLED] ?: true,
                backgroundTrackingEnabled = prefs[Keys.BG_TRACKING] ?: true,
                calibratedStrideMeters = prefs[Keys.CALIBRATED_STRIDE] ?: (currentHeight * 0.00415),
                onboardingCompleted = prefs[Keys.ONBOARDING_DONE] ?: false
            )
            val updated = transform(current)
            prefs[Keys.HEIGHT_CM] = updated.heightCm
            prefs[Keys.WEIGHT_KG] = updated.weightKg
            prefs[Keys.AGE] = updated.age
            prefs[Keys.SEX] = updated.sex.name
            prefs[Keys.DAILY_GOAL] = updated.dailyGoal
            prefs[Keys.UNIT_SYSTEM] = updated.unitSystem.name
            prefs[Keys.THEME] = updated.theme.name
            prefs[Keys.GPS_ENABLED] = updated.gpsEnabled
            prefs[Keys.BG_TRACKING] = updated.backgroundTrackingEnabled
            prefs[Keys.CALIBRATED_STRIDE] = updated.calibratedStrideMeters
            prefs[Keys.ONBOARDING_DONE] = updated.onboardingCompleted
        }
    }
}
""",

    "app/src/main/java/com/stride/app/data/sensor/SensorDataSource.kt": """package com.stride.app.data.sensor

import android.content.Context
import android.hardware.Sensor
import android.hardware.SensorEvent
import android.hardware.SensorEventListener
import android.hardware.SensorManager
import dagger.hilt.android.qualifiers.ApplicationContext
import kotlinx.coroutines.channels.awaitClose
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.callbackFlow
import javax.inject.Inject
import javax.inject.Singleton

sealed interface RawSensorEvent {
    data class HardwareStepCounter(val rawTotalSteps: Long, val timestampMs: Long) : RawSensorEvent
    data class StepDetectorPulse(val timestampMs: Long) : RawSensorEvent
    data class Accelerometer(val ax: Float, val ay: Float, val az: Float, val timestampMs: Long) : RawSensorEvent
    data class Gyroscope(val gx: Float, val gy: Float, val gz: Float) : RawSensorEvent
}

@Singleton
class SensorDataSource @Inject constructor(
    @ApplicationContext context: Context
) {
    private val sensorManager = context.getSystemService(Context.SENSOR_SERVICE) as SensorManager

    val hasHardwareStepCounter: Boolean
        get() = sensorManager.getDefaultSensor(Sensor.TYPE_STEP_COUNTER) != null

    fun observeSensors(activeSessionMode: Boolean): Flow<RawSensorEvent> = callbackFlow {
        val listener = object : SensorEventListener {
            override fun onSensorChanged(event: SensorEvent) {
                val nowMs = System.currentTimeMillis()
                when (event.sensor.type) {
                    Sensor.TYPE_STEP_COUNTER -> {
                        trySend(RawSensorEvent.HardwareStepCounter(event.values[0].toLong(), nowMs))
                    }
                    Sensor.TYPE_STEP_DETECTOR -> {
                        trySend(RawSensorEvent.StepDetectorPulse(nowMs))
                    }
                    Sensor.TYPE_ACCELEROMETER -> {
                        trySend(
                            RawSensorEvent.Accelerometer(
                                event.values[0],
                                event.values[1],
                                event.values[2],
                                nowMs
                            )
                        )
                    }
                    Sensor.TYPE_GYROSCOPE -> {
                        trySend(
                            RawSensorEvent.Gyroscope(
                                event.values[0],
                                event.values[1],
                                event.values[2]
                            )
                        )
                    }
                }
            }

            override fun onAccuracyChanged(sensor: Sensor?, accuracy: Int) = Unit
        }

        val stepCounter = sensorManager.getDefaultSensor(Sensor.TYPE_STEP_COUNTER)
        val stepDetector = sensorManager.getDefaultSensor(Sensor.TYPE_STEP_DETECTOR)
        val accelerometer = sensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER)
        val gyroscope = sensorManager.getDefaultSensor(Sensor.TYPE_GYROSCOPE)

        val batchLatencyUs = if (activeSessionMode) 0 else 5_000_000
        val rate = if (activeSessionMode) SensorManager.SENSOR_DELAY_GAME else SensorManager.SENSOR_DELAY_NORMAL

        if (stepCounter != null) {
            sensorManager.registerListener(listener, stepCounter, rate, batchLatencyUs)
        }
        if (stepDetector != null) {
            sensorManager.registerListener(listener, stepDetector, rate, batchLatencyUs)
        }
        if (activeSessionMode || stepCounter == null) {
            accelerometer?.let { sensorManager.registerListener(listener, it, SensorManager.SENSOR_DELAY_GAME) }
            gyroscope?.let { sensorManager.registerListener(listener, it, SensorManager.SENSOR_DELAY_NORMAL) }
        }

        awaitClose {
            sensorManager.unregisterListener(listener)
        }
    }
}
""",

    "app/src/main/java/com/stride/app/data/location/LocationDataSource.kt": """package com.stride.app.data.location

import android.annotation.SuppressLint
import android.content.Context
import android.location.Location
import android.os.Looper
import com.google.android.gms.location.LocationCallback
import com.google.android.gms.location.LocationRequest
import com.google.android.gms.location.LocationResult
import com.google.android.gms.location.LocationServices
import com.google.android.gms.location.Priority
import dagger.hilt.android.qualifiers.ApplicationContext
import kotlinx.coroutines.channels.awaitClose
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.callbackFlow
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class LocationDataSource @Inject constructor(
    @ApplicationContext private val context: Context
) {
    private val fusedClient = LocationServices.getFusedLocationProviderClient(context)

    @SuppressLint("MissingPermission")
    fun observeHighAccuracyLocations(): Flow<Location> = callbackFlow {
        val request = LocationRequest.Builder(Priority.PRIORITY_HIGH_ACCURACY, 2000L)
            .setMinUpdateIntervalMillis(1000L)
            .setMinUpdateDistanceMeters(1.5f)
            .build()

        val callback = object : LocationCallback() {
            override fun onLocationResult(result: LocationResult) {
                for (location in result.locations) {
                    trySend(location)
                }
            }
        }

        try {
            fusedClient.requestLocationUpdates(request, callback, Looper.getMainLooper())
        } catch (se: SecurityException) {
            close()
        }

        awaitClose {
            fusedClient.removeLocationUpdates(callback)
        }
    }
}
""",

    "app/src/main/java/com/stride/app/data/repository/StrideRepository.kt": """package com.stride.app.data.repository

import android.app.NotificationChannel
import android.app.NotificationManager
import android.content.Context
import androidx.core.app.NotificationCompat
import com.stride.app.R
import com.stride.app.data.datastore.UserPreferencesRepository
import com.stride.app.data.local.ActivitySessionEntity
import com.stride.app.data.local.DailyStepEntity
import com.stride.app.data.local.StrideDao
import com.stride.app.domain.engine.DayRolloverCalculator
import com.stride.app.domain.engine.StepFusionEngine
import com.stride.app.domain.model.ActivitySession
import com.stride.app.domain.model.ActivityType
import com.stride.app.domain.model.DailySummary
import com.stride.app.domain.model.LiveSessionState
import com.stride.app.domain.model.UserProfile
import com.stride.app.domain.usecase.CalculateStatsUseCase
import com.stride.app.widget.StrideWidget
import dagger.hilt.android.qualifiers.ApplicationContext
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import java.time.LocalDate
import java.time.LocalTime
import javax.inject.Inject
import javax.inject.Singleton
import kotlin.math.roundToInt

@Singleton
class StrideRepository @Inject constructor(
    @ApplicationContext private val context: Context,
    private val dao: StrideDao,
    private val prefs: UserPreferencesRepository,
    private val statsUseCase: CalculateStatsUseCase
) {
    private val repoScope = CoroutineScope(SupervisorJob() + Dispatchers.IO)
    val fusionEngine = StepFusionEngine()

    private val _liveSession = MutableStateFlow(LiveSessionState())
    val liveSession: StateFlow<LiveSessionState> = _liveSession.asStateFlow()

    private var sessionStartEpochMs: Long = 0L
    private var lastKmSplitDistance: Double = 0.0
    private var lastKmSplitDurationSec: Long = 0L

    init {
        repoScope.launch {
            prefs.userProfileFlow.collect { profile ->
                ensureTodayExists(profile)
            }
        }
    }

    val userProfileFlow: Flow<UserProfile> = prefs.userProfileFlow

    fun observeTodaySummary(): Flow<DailySummary> {
        val today = LocalDate.now().toEpochDay()
        return dao.observeDay(today).map { entity ->
            entity?.toDomain() ?: DailySummary(
                dateEpochDay = today,
                steps = 0,
                goal = 10000,
                distanceMeters = 0.0,
                caloriesKcal = 0,
                activeMinutes = 0
            )
        }
    }

    fun observeAllDays(): Flow<List<DailySummary>> =
        dao.observeAllDays().map { list -> list.map { it.toDomain() } }

    fun observeAllSessions(): Flow<List<ActivitySession>> =
        dao.observeAllSessions().map { list -> list.map { it.toDomain() } }

    suspend fun getSessionById(id: Long): ActivitySession? =
        dao.getSessionById(id)?.toDomain()

    suspend fun ensureTodayExists(profile: UserProfile? = null): DailyStepEntity {
        val p = profile ?: prefs.userProfileFlow.first()
        val today = LocalDate.now().toEpochDay()
        val existing = dao.getDay(today)
        if (existing != null) {
            if (existing.goal != p.dailyGoal) {
                val updated = existing.copy(goal = p.dailyGoal)
                dao.upsertDay(updated)
                return updated
            }
            return existing
        }
        val fresh = DailyStepEntity(
            dateEpochDay = today,
            steps = 0,
            goal = p.dailyGoal,
            distanceMeters = 0.0,
            caloriesKcal = 0,
            activeMinutes = 0,
            lastHardwareCounter = 0L,
            hourlyStepsCsv = List(24) { 0 }.joinToString(","),
            goalNotified = false
        )
        dao.upsertDay(fresh)
        return fresh
    }

    suspend fun onHardwareStepCounter(rawSteps: Long, timestampMs: Long) {
        val deltaFromEngine = fusionEngine.processHardwareStepCounter(rawSteps, timestampMs)
        val todayEpoch = LocalDate.now().toEpochDay()
        val profile = prefs.userProfileFlow.first()
        val existing = dao.getDay(todayEpoch)

        val snapshot = existing?.let {
            DayRolloverCalculator.CounterSnapshot(
                dateEpochDay = it.dateEpochDay,
                savedStepsToday = it.steps,
                lastHardwareReading = it.lastHardwareCounter
            )
        }

        val reconciled = DayRolloverCalculator.reconcile(
            snapshot = snapshot,
            currentEpochDay = todayEpoch,
            currentHardwareSteps = rawSteps
        )

        val effectiveDelta = if (existing == null || existing.lastHardwareCounter == 0L) {
            deltaFromEngine
        } else {
            reconciled.deltaAdded.coerceAtMost(500)
        }

        if (effectiveDelta > 0 || existing == null || existing.lastHardwareCounter == 0L) {
            applyStepsDelta(
                deltaSteps = effectiveDelta,
                newHardwareBaseline = rawSteps,
                profile = profile
            )
        }
    }

    suspend fun onValidatedSoftwareSteps(deltaSteps: Int) {
        if (deltaSteps <= 0) return
        val profile = prefs.userProfileFlow.first()
        applyStepsDelta(deltaSteps = deltaSteps, newHardwareBaseline = null, profile = profile)
    }

    private suspend fun applyStepsDelta(
        deltaSteps: Int,
        newHardwareBaseline: Long?,
        profile: UserProfile
    ) {
        val currentEntity = ensureTodayExists(profile)
        val newSteps = currentEntity.steps + deltaSteps
        val hour = LocalTime.now().hour.coerceIn(0, 23)
        val hourly = currentEntity.hourlyStepsCsv.split(",")
            .mapNotNull { it.trim().toIntOrNull() }
            .toMutableList()
            .apply {
                while (size < 24) add(0)
                this[hour] = this[hour] + deltaSteps
            }

        val distance = fusionEngine.estimateDistanceMeters(newSteps)
        val calories = statsUseCase.estimateCaloriesFromSteps(newSteps, profile)
        val activeMin = statsUseCase.estimateActiveMinutes(newSteps)

        val shouldNotifyGoal = !currentEntity.goalNotified && newSteps >= profile.dailyGoal
        if (shouldNotifyGoal) {
            sendGoalReachedNotification(newSteps, profile.dailyGoal)
        }

        val updated = currentEntity.copy(
            steps = newSteps,
            goal = profile.dailyGoal,
            distanceMeters = distance,
            caloriesKcal = calories,
            activeMinutes = activeMin,
            lastHardwareCounter = newHardwareBaseline ?: currentEntity.lastHardwareCounter,
            hourlyStepsCsv = hourly.joinToString(","),
            goalNotified = currentEntity.goalNotified || shouldNotifyGoal
        )
        dao.upsertDay(updated)

        if (_liveSession.value.isActive && !_liveSession.value.isPaused && deltaSteps > 0) {
            _liveSession.update { state ->
                val newSessionSteps = state.steps + deltaSteps
                val fallbackDist = if (!profile.gpsEnabled || state.route.isEmpty()) {
                    state.distanceMeters + fusionEngine.estimateDistanceMeters(deltaSteps)
                } else {
                    state.distanceMeters
                }
                state.copy(
                    steps = newSessionSteps,
                    distanceMeters = fallbackDist,
                    cadenceSpm = fusionEngine.getCurrentCadenceSpm()
                )
            }
        }

        StrideWidget.updateAllWidgets(context, newSteps, profile.dailyGoal)
    }

    fun startSession(type: ActivityType) {
        fusionEngine.resetSessionGpsState()
        sessionStartEpochMs = System.currentTimeMillis()
        lastKmSplitDistance = 0.0
        lastKmSplitDurationSec = 0L
        _liveSession.value = LiveSessionState(
            isActive = true,
            isPaused = false,
            type = type
        )
    }

    fun pauseSession() {
        _liveSession.update { it.copy(isPaused = true, currentSpeedMps = 0.0, cadenceSpm = 0) }
    }

    fun resumeSession() {
        _liveSession.update { it.copy(isPaused = false) }
    }

    suspend fun tickSessionTimer(profile: UserProfile) {
        val state = _liveSession.value
        if (!state.isActive || state.isPaused) return
        val newDuration = state.durationSeconds + 1
        val calories = statsUseCase.estimateSessionCalories(state.type, newDuration, profile.weightKg)
        val paceSecPerKm = if (state.distanceMeters > 15.0) {
            ((newDuration.toDouble() / (state.distanceMeters / 1000.0))).roundToInt().coerceIn(120, 3600)
        } else 0

        _liveSession.update {
            it.copy(
                durationSeconds = newDuration,
                caloriesKcal = calories,
                currentPaceSecPerKm = paceSecPerKm,
                cadenceSpm = fusionEngine.getCurrentCadenceSpm(System.currentTimeMillis())
            )
        }
    }

    suspend fun onGpsLocationUpdate(
        lat: Double,
        lng: Double,
        accuracyMeters: Float,
        speedMps: Float,
        timestampMs: Long
    ) {
        val state = _liveSession.value
        if (!state.isActive || state.isPaused) return

        val result = fusionEngine.processGpsLocation(
            lat = lat,
            lng = lng,
            accuracyMeters = accuracyMeters,
            speedMps = speedMps,
            timestampMs = timestampMs,
            stepsSinceLastFix = 3
        )
        if (!result.accepted || result.smoothedPoint == null) return

        val newDist = state.distanceMeters + result.deltaDistanceMeters
        val splits = state.paceHistorySecPerKm.toMutableList()
        if (newDist - lastKmSplitDistance >= 200.0) {
            val dt = (state.durationSeconds - lastKmSplitDurationSec).coerceAtLeast(1L)
            val dKm = (newDist - lastKmSplitDistance) / 1000.0
            val splitPace = (dt / dKm).roundToInt().coerceIn(120, 2400)
            splits.add(splitPace)
            lastKmSplitDistance = newDist
            lastKmSplitDurationSec = state.durationSeconds
        }

        prefs.updateProfile { it.copy(calibratedStrideMeters = fusionEngine.strideLengthMeters) }

        _liveSession.update {
            it.copy(
                distanceMeters = newDist,
                currentSpeedMps = speedMps.toDouble(),
                route = it.route + result.smoothedPoint,
                paceHistorySecPerKm = splits
            )
        }
    }

    suspend fun stopAndSaveSession(): Long? {
        val state = _liveSession.value
        if (!state.isActive) return null
        _liveSession.value = LiveSessionState(isActive = false)

        if (state.durationSeconds < 3 && state.steps < 5 && state.distanceMeters < 5.0) {
            return null
        }

        val avgSpeed = if (state.durationSeconds > 0) {
            state.distanceMeters / state.durationSeconds
        } else 0.0
        val avgPace = if (state.distanceMeters > 10.0) {
            (state.durationSeconds / (state.distanceMeters / 1000.0)).roundToInt()
        } else 0
        val avgCadence = if (state.durationSeconds > 0) {
            ((state.steps * 60.0) / state.durationSeconds).roundToInt()
        } else 0

        val session = ActivitySession(
            type = state.type,
            startTimeMs = sessionStartEpochMs,
            endTimeMs = System.currentTimeMillis(),
            durationSeconds = state.durationSeconds,
            steps = state.steps,
            distanceMeters = state.distanceMeters,
            caloriesKcal = state.caloriesKcal,
            avgPaceSecPerKm = avgPace,
            avgSpeedMps = avgSpeed,
            avgCadenceSpm = avgCadence,
            routePoints = state.route,
            paceSplitsSecPerKm = if (state.paceHistorySecPerKm.isNotEmpty()) {
                state.paceHistorySecPerKm
            } else if (avgPace > 0) {
                listOf(avgPace)
            } else {
                listOf(600)
            }
        )
        return dao.insertSession(ActivitySessionEntity.fromDomain(session))
    }

    suspend fun getAllDaysSnapshot(): List<DailySummary> =
        dao.getAllDays().map { it.toDomain() }

    suspend fun getAllSessionsSnapshot(): List<ActivitySession> =
        dao.getAllSessions().map { it.toDomain() }

    suspend fun deleteAllData() {
        dao.deleteAllDays()
        dao.deleteAllSessions()
        ensureTodayExists()
    }

    private fun sendGoalReachedNotification(steps: Int, goal: Int) {
        val nm = context.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
        val channelId = "stride_goal_channel"
        val channel = NotificationChannel(
            channelId,
            "Daily Goal",
            NotificationManager.IMPORTANCE_DEFAULT
        )
        nm.createNotificationChannel(channel)

        val notification = NotificationCompat.Builder(context, channelId)
            .setSmallIcon(R.drawable.ic_launcher_foreground)
            .setContentTitle("Daily Goal Reached")
            .setContentText("You hit $steps steps today (Goal: $goal). Keep moving!")
            .setAutoCancel(true)
            .build()

        nm.notify(2002, notification)
    }
}
""",

    "app/src/main/java/com/stride/app/di/AppModule.kt": """package com.stride.app.di

import android.content.Context
import androidx.room.Room
import com.stride.app.data.local.StrideDao
import com.stride.app.data.local.StrideDatabase
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.android.qualifiers.ApplicationContext
import dagger.hilt.components.SingletonComponent
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
object AppModule {

    @Provides
    @Singleton
    fun provideDatabase(@ApplicationContext context: Context): StrideDatabase {
        return Room.databaseBuilder(
            context,
            StrideDatabase::class.java,
            "stride_db"
        ).fallbackToDestructiveMigration().build()
    }

    @Provides
    fun provideStrideDao(db: StrideDatabase): StrideDao = db.strideDao()
}
""",

    "app/src/main/java/com/stride/app/service/TrackingService.kt": """package com.stride.app.service

import android.Manifest
import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.app.Service
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.content.pm.ServiceInfo
import android.os.Build
import android.os.IBinder
import androidx.core.app.NotificationCompat
import androidx.core.content.ContextCompat
import com.stride.app.MainActivity
import com.stride.app.R
import com.stride.app.data.location.LocationDataSource
import com.stride.app.data.repository.StrideRepository
import com.stride.app.data.sensor.RawSensorEvent
import com.stride.app.data.sensor.SensorDataSource
import com.stride.app.domain.model.ActivityType
import dagger.hilt.android.AndroidEntryPoint
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.cancel
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.isActive
import kotlinx.coroutines.launch
import javax.inject.Inject

@AndroidEntryPoint
class TrackingService : Service() {

    companion object {
        const val ACTION_START_PASSIVE = "com.stride.app.action.START_PASSIVE"
        const val ACTION_START_SESSION = "com.stride.app.action.START_SESSION"
        const val ACTION_PAUSE_SESSION = "com.stride.app.action.PAUSE_SESSION"
        const val ACTION_RESUME_SESSION = "com.stride.app.action.RESUME_SESSION"
        const val ACTION_STOP_SESSION = "com.stride.app.action.STOP_SESSION"
        const val EXTRA_ACTIVITY_TYPE = "extra_activity_type"

        private const val NOTIFICATION_ID = 1001
        private const val CHANNEL_ID = "stride_tracking_channel"

        fun startPassive(context: Context) {
            val intent = Intent(context, TrackingService::class.java).apply {
                action = ACTION_START_PASSIVE
            }
            ContextCompat.startForegroundService(context, intent)
        }

        fun startSession(context: Context, type: ActivityType) {
            val intent = Intent(context, TrackingService::class.java).apply {
                action = ACTION_START_SESSION
                putExtra(EXTRA_ACTIVITY_TYPE, type.name)
            }
            ContextCompat.startForegroundService(context, intent)
        }

        fun sendCommand(context: Context, action: String) {
            val intent = Intent(context, TrackingService::class.java).apply {
                this.action = action
            }
            context.startService(intent)
        }
    }

    @Inject lateinit var repository: StrideRepository
    @Inject lateinit var sensorDataSource: SensorDataSource
    @Inject lateinit var locationDataSource: LocationDataSource

    private val serviceScope = CoroutineScope(SupervisorJob() + Dispatchers.Default)
    private var sensorJob: Job? = null
    private var locationJob: Job? = null
    private var timerJob: Job? = null

    override fun onCreate() {
        super.onCreate()
        createNotificationChannel()
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        when (intent?.action) {
            ACTION_START_SESSION -> {
                val typeName = intent.getStringExtra(EXTRA_ACTIVITY_TYPE) ?: ActivityType.WALK.name
                val type = runCatching { ActivityType.valueOf(typeName) }.getOrDefault(ActivityType.WALK)
                repository.startSession(type)
                promoteToForeground(isSessionActive = true)
                startSensorCollection(activeSessionMode = true)
                startSessionLoop()
            }
            ACTION_PAUSE_SESSION -> {
                repository.pauseSession()
                updateNotification()
            }
            ACTION_RESUME_SESSION -> {
                repository.resumeSession()
                updateNotification()
            }
            ACTION_STOP_SESSION -> {
                serviceScope.launch {
                    repository.stopAndSaveSession()
                    locationJob?.cancel()
                    timerJob?.cancel()
                    val profile = repository.userProfileFlow.first()
                    if (profile.backgroundTrackingEnabled) {
                        startSensorCollection(activeSessionMode = false)
                        updateNotification()
                    } else {
                        stopForeground(STOP_FOREGROUND_REMOVE)
                        stopSelf()
                    }
                }
            }
            else -> {
                promoteToForeground(isSessionActive = false)
                startSensorCollection(activeSessionMode = false)
            }
        }
        return START_STICKY
    }

    private fun promoteToForeground(isSessionActive: Boolean) {
        val notification = buildNotification()
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.UPSIDE_DOWN_CAKE) {
            val hasLoc = ContextCompat.checkSelfPermission(
                this,
                Manifest.permission.ACCESS_FINE_LOCATION
            ) == PackageManager.PERMISSION_GRANTED
            val fgType = if (isSessionActive && hasLoc) {
                ServiceInfo.FOREGROUND_SERVICE_TYPE_HEALTH or ServiceInfo.FOREGROUND_SERVICE_TYPE_LOCATION
            } else {
                ServiceInfo.FOREGROUND_SERVICE_TYPE_HEALTH
            }
            startForeground(NOTIFICATION_ID, notification, fgType)
        } else {
            startForeground(NOTIFICATION_ID, notification)
        }
    }

    private fun startSensorCollection(activeSessionMode: Boolean) {
        sensorJob?.cancel()
        sensorJob = serviceScope.launch {
            val useHardwareCounter = sensorDataSource.hasHardwareStepCounter
            sensorDataSource.observeSensors(activeSessionMode).collect { event ->
                when (event) {
                    is RawSensorEvent.HardwareStepCounter -> {
                        repository.onHardwareStepCounter(event.rawTotalSteps, event.timestampMs)
                        if (repository.liveSession.value.isActive) updateNotification()
                    }
                    is RawSensorEvent.Gyroscope -> {
                        repository.fusionEngine.processGyroscope(event.gx, event.gy, event.gz)
                    }
                    is RawSensorEvent.Accelerometer -> {
                        val validated = repository.fusionEngine.processAccelerometer(
                            event.ax, event.ay, event.az, event.timestampMs
                        )
                        if (!useHardwareCounter && validated > 0) {
                            repository.onValidatedSoftwareSteps(validated)
                            if (repository.liveSession.value.isActive) updateNotification()
                        }
                    }
                    is RawSensorEvent.StepDetectorPulse -> {
                        if (!useHardwareCounter) {
                            repository.onValidatedSoftwareSteps(1)
                        }
                    }
                }
            }
        }
    }

    private fun startSessionLoop() {
        timerJob?.cancel()
        timerJob = serviceScope.launch {
            while (isActive && repository.liveSession.value.isActive) {
                val profile = repository.userProfileFlow.first()
                repository.tickSessionTimer(profile)
                updateNotification()
                delay(1000L)
            }
        }

        locationJob?.cancel()
        locationJob = serviceScope.launch {
            val profile = repository.userProfileFlow.first()
            val hasLocationPerm = ContextCompat.checkSelfPermission(
                this@TrackingService,
                Manifest.permission.ACCESS_FINE_LOCATION
            ) == PackageManager.PERMISSION_GRANTED

            if (profile.gpsEnabled && hasLocationPerm) {
                locationDataSource.observeHighAccuracyLocations().collect { loc ->
                    repository.onGpsLocationUpdate(
                        lat = loc.latitude,
                        lng = loc.longitude,
                        accuracyMeters = loc.accuracy,
                        speedMps = loc.speed,
                        timestampMs = loc.time
                    )
                }
            }
        }
    }

    private fun updateNotification() {
        val nm = getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
        nm.notify(NOTIFICATION_ID, buildNotification())
    }

    private fun buildNotification(): Notification {
        val openAppIntent = PendingIntent.getActivity(
            this,
            0,
            Intent(this, MainActivity::class.java),
            PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT
        )

        val session = repository.liveSession.value
        val builder = NotificationCompat.Builder(this, CHANNEL_ID)
            .setSmallIcon(R.drawable.ic_launcher_foreground)
            .setContentIntent(openAppIntent)
            .setOngoing(true)
            .setOnlyAlertOnce(true)
            .setSilent(true)

        if (session.isActive) {
            val distKm = "%.2f km".format(session.distanceMeters / 1000.0)
            val mins = session.durationSeconds / 60
            val secs = session.durationSeconds % 60
            val timeStr = "%02d:%02d".format(mins, secs)

            builder.setContentTitle("${session.type.label} • $timeStr")
            builder.setContentText("${session.steps} steps • $distKm")

            val toggleAction = if (session.isPaused) {
                NotificationCompat.Action(
                    0,
                    "Resume",
                    servicePendingIntent(ACTION_RESUME_SESSION, 1)
                )
            } else {
                NotificationCompat.Action(
                    0,
                    "Pause",
                    servicePendingIntent(ACTION_PAUSE_SESSION, 2)
                )
            }
            val stopAction = NotificationCompat.Action(
                0,
                "Stop",
                servicePendingIntent(ACTION_STOP_SESSION, 3)
            )
            builder.addAction(toggleAction)
            builder.addAction(stopAction)
        } else {
            builder.setContentTitle("Stride Passive Tracking")
            builder.setContentText("Counting daily steps in low-power mode")
        }

        return builder.build()
    }

    private fun servicePendingIntent(action: String, requestCode: Int): PendingIntent {
        val intent = Intent(this, TrackingService::class.java).apply { this.action = action }
        return PendingIntent.getService(
            this,
            requestCode,
            intent,
            PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT
        )
    }

    private fun createNotificationChannel() {
        val nm = getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
        val channel = NotificationChannel(
            CHANNEL_ID,
            "Step & Workout Tracking",
            NotificationManager.IMPORTANCE_LOW
        ).apply {
            description = "Shows live workout metrics and passive step tracking status"
        }
        nm.createNotificationChannel(channel)
    }

    override fun onDestroy() {
        serviceScope.cancel()
        super.onDestroy()
    }

    override fun onBind(intent: Intent?): IBinder? = null
}
""",

    "app/src/main/java/com/stride/app/service/BootReceiver.kt": """package com.stride.app.service

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import com.stride.app.data.datastore.UserPreferencesRepository
import dagger.hilt.android.AndroidEntryPoint
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.launch
import javax.inject.Inject

@AndroidEntryPoint
class BootReceiver : BroadcastReceiver() {

    @Inject lateinit var prefs: UserPreferencesRepository

    override fun onReceive(context: Context, intent: Intent) {
        if (intent.action == Intent.ACTION_BOOT_COMPLETED ||
            intent.action == Intent.ACTION_MY_PACKAGE_REPLACED
        ) {
            DailyRolloverWorker.schedule(context)
            CoroutineScope(Dispatchers.IO).launch {
                val profile = prefs.userProfileFlow.first()
                if (profile.onboardingCompleted && profile.backgroundTrackingEnabled) {
                    TrackingService.startPassive(context)
                }
            }
        }
    }
}
""",

    "app/src/main/java/com/stride/app/service/ActivityRecognitionReceiver.kt": """package com.stride.app.service

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import com.google.android.gms.location.ActivityRecognitionResult
import com.google.android.gms.location.DetectedActivity
import com.stride.app.data.repository.StrideRepository
import dagger.hilt.android.AndroidEntryPoint
import javax.inject.Inject

@AndroidEntryPoint
class ActivityRecognitionReceiver : BroadcastReceiver() {

    @Inject lateinit var repository: StrideRepository

    override fun onReceive(context: Context, intent: Intent) {
        if (ActivityRecognitionResult.hasResult(intent)) {
            val result = ActivityRecognitionResult.extractResult(intent) ?: return
            val mostProbable = result.mostProbableActivity
            val inVehicle = mostProbable.type == DetectedActivity.IN_VEHICLE && mostProbable.confidence >= 60
            val isStill = mostProbable.type == DetectedActivity.STILL && mostProbable.confidence >= 75
            repository.fusionEngine.setActivityRecognitionState(inVehicle = inVehicle, still = isStill)
        }
    }
}
""",

    "app/src/main/java/com/stride/app/service/DailyRolloverWorker.kt": """package com.stride.app.service

import android.content.Context
import androidx.hilt.work.HiltWorker
import androidx.work.CoroutineWorker
import androidx.work.ExistingPeriodicWorkPolicy
import androidx.work.PeriodicWorkRequestBuilder
import androidx.work.WorkManager
import androidx.work.WorkerParameters
import com.stride.app.data.repository.StrideRepository
import com.stride.app.widget.StrideWidget
import dagger.assisted.Assisted
import dagger.assisted.AssistedInject
import java.util.concurrent.TimeUnit

@HiltWorker
class DailyRolloverWorker @AssistedInject constructor(
    @Assisted private val appContext: Context,
    @Assisted workerParams: WorkerParameters,
    private val repository: StrideRepository
) : CoroutineWorker(appContext, workerParams) {

    override suspend fun doWork(): Result {
        val todayEntity = repository.ensureTodayExists()
        StrideWidget.updateAllWidgets(appContext, todayEntity.steps, todayEntity.goal)
        return Result.success()
    }

    companion object {
        private const val WORK_NAME = "stride_daily_rollover_work"

        fun schedule(context: Context) {
            val request = PeriodicWorkRequestBuilder<DailyRolloverWorker>(
                15, TimeUnit.MINUTES
            ).build()
            WorkManager.getInstance(context).enqueueUniquePeriodicWork(
                WORK_NAME,
                ExistingPeriodicWorkPolicy.KEEP,
                request
            )
        }
    }
}
""",

    "app/src/main/java/com/stride/app/widget/StrideWidget.kt": """package com.stride.app.widget

import android.content.Context
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.datastore.preferences.core.Preferences
import androidx.datastore.preferences.core.intPreferencesKey
import androidx.glance.GlanceId
import androidx.glance.GlanceModifier
import androidx.glance.GlanceTheme
import androidx.glance.action.actionStartActivity
import androidx.glance.action.clickable
import androidx.glance.appwidget.GlanceAppWidget
import androidx.glance.appwidget.GlanceAppWidgetManager
import androidx.glance.appwidget.provideContent
import androidx.glance.appwidget.state.updateAppWidgetState
import androidx.glance.background
import androidx.glance.currentState
import androidx.glance.layout.Alignment
import androidx.glance.layout.Box
import androidx.glance.layout.Column
import androidx.glance.layout.Spacer
import androidx.glance.layout.fillMaxSize
import androidx.glance.layout.height
import androidx.glance.layout.padding
import androidx.glance.state.GlanceStateDefinition
import androidx.glance.state.PreferencesGlanceStateDefinition
import androidx.glance.text.FontWeight
import androidx.glance.text.Text
import androidx.glance.text.TextStyle
import androidx.glance.unit.ColorProvider
import com.stride.app.MainActivity
import java.text.NumberFormat
import java.util.Locale

class StrideWidget : GlanceAppWidget() {

    override val stateDefinition: GlanceStateDefinition<*> = PreferencesGlanceStateDefinition

    override suspend fun provideGlance(context: Context, id: GlanceId) {
        provideContent {
            val prefs = currentState<Preferences>()
            val steps = prefs[KEY_STEPS] ?: 0
            val goal = prefs[KEY_GOAL] ?: 10000
            GlanceTheme {
                WidgetContent(steps = steps, goal = goal)
            }
        }
    }

    @Composable
    private fun WidgetContent(steps: Int, goal: Int) {
        val pct = if (goal > 0) ((steps.toFloat() / goal) * 100).toInt().coerceIn(0, 100) else 0
        Box(
            modifier = GlanceModifier
                .fillMaxSize()
                .background(ColorProvider(Color(0xFF0E1110)))
                .padding(14.dp)
                .clickable(actionStartActivity<MainActivity>()),
            contentAlignment = Alignment.Center
        ) {
            Column(
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                Text(
                    text = "STRIDE",
                    style = TextStyle(
                        color = ColorProvider(Color(0xFF0F9D7A)),
                        fontSize = 11.sp,
                        fontWeight = FontWeight.Bold
                    )
                )
                Spacer(modifier = GlanceModifier.height(6.dp))
                Text(
                    text = NumberFormat.getIntegerInstance(Locale.getDefault()).format(steps),
                    style = TextStyle(
                        color = ColorProvider(Color(0xFFF7F8F7)),
                        fontSize = 26.sp,
                        fontWeight = FontWeight.Bold
                    )
                )
                Spacer(modifier = GlanceModifier.height(2.dp))
                Text(
                    text = "$pct% of ${NumberFormat.getIntegerInstance(Locale.getDefault()).format(goal)}",
                    style = TextStyle(
                        color = ColorProvider(Color(0xFF8C9692)),
                        fontSize = 12.sp
                    )
                )
            }
        }
    }

    companion object {
        val KEY_STEPS = intPreferencesKey("widget_steps")
        val KEY_GOAL = intPreferencesKey("widget_goal")

        suspend fun updateAllWidgets(context: Context, steps: Int, goal: Int) {
            val manager = GlanceAppWidgetManager(context)
            val glanceIds = manager.getGlanceIds(StrideWidget::class.java)
            glanceIds.forEach { id ->
                updateAppWidgetState(context, PreferencesGlanceStateDefinition, id) { prefs ->
                    prefs.toMutablePreferences().apply {
                        this[KEY_STEPS] = steps
                        this[KEY_GOAL] = goal
                    }
                }
                StrideWidget().update(context, id)
            }
        }
    }
}
""",

    "app/src/main/java/com/stride/app/widget/StrideWidgetReceiver.kt": """package com.stride.app.widget

import androidx.glance.appwidget.GlanceAppWidget
import androidx.glance.appwidget.GlanceAppWidgetReceiver

class StrideWidgetReceiver : GlanceAppWidgetReceiver() {
    override val glanceAppWidget: GlanceAppWidget = StrideWidget()
}
""",

    "app/src/main/java/com/stride/app/ui/theme/Color.kt": """package com.stride.app.ui.theme

import androidx.compose.ui.graphics.Color

val EmeraldPrimary = Color(0xFF0F9D7A)
val EmeraldSecondary = Color(0xFF14B890)
val EmeraldSubtle = Color(0xFF0F9D7A).copy(alpha = 0.14f)

val LightBackground = Color(0xFFF7F8F7)
val LightSurface = Color(0xFFFFFFFF)
val LightOutline = Color(0xFFE2E7E4)
val LightTextPrimary = Color(0xFF0E1110)
val LightTextSecondary = Color(0xFF5F6B66)

val DarkBackground = Color(0xFF0E1110)
val DarkSurface = Color(0xFF161B19)
val DarkOutline = Color(0xFF242C29)
val DarkTextPrimary = Color(0xFFF7F8F7)
val DarkTextSecondary = Color(0xFF8C9692)

val SemanticSuccess = Color(0xFF0F9D7A)
val SemanticError = Color(0xFFD9534F)
""",

    "app/src/main/java/com/stride/app/ui/theme/Type.kt": """package com.stride.app.ui.theme

import androidx.compose.material3.Typography
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.sp

val StrideTypography = Typography(
    displayLarge = TextStyle(
        fontFamily = FontFamily.SansSerif,
        fontWeight = FontWeight.Medium,
        fontSize = 60.sp,
        lineHeight = 64.sp,
        letterSpacing = (-1.5).sp
    ),
    displayMedium = TextStyle(
        fontFamily = FontFamily.SansSerif,
        fontWeight = FontWeight.Medium,
        fontSize = 44.sp,
        lineHeight = 48.sp,
        letterSpacing = (-1.0).sp
    ),
    headlineMedium = TextStyle(
        fontFamily = FontFamily.SansSerif,
        fontWeight = FontWeight.SemiBold,
        fontSize = 24.sp,
        lineHeight = 30.sp
    ),
    titleMedium = TextStyle(
        fontFamily = FontFamily.SansSerif,
        fontWeight = FontWeight.Medium,
        fontSize = 18.sp,
        lineHeight = 24.sp
    ),
    bodyLarge = TextStyle(
        fontFamily = FontFamily.SansSerif,
        fontWeight = FontWeight.Normal,
        fontSize = 16.sp,
        lineHeight = 24.sp
    ),
    bodyMedium = TextStyle(
        fontFamily = FontFamily.SansSerif,
        fontWeight = FontWeight.Normal,
        fontSize = 14.sp,
        lineHeight = 20.sp
    ),
    labelSmall = TextStyle(
        fontFamily = FontFamily.SansSerif,
        fontWeight = FontWeight.SemiBold,
        fontSize = 11.sp,
        lineHeight = 14.sp,
        letterSpacing = 1.1.sp
    )
)
""",

    "app/src/main/java/com/stride/app/ui/theme/Theme.kt": """package com.stride.app.ui.theme

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import com.stride.app.domain.model.AppTheme

private val DarkColors = darkColorScheme(
    primary = EmeraldPrimary,
    onPrimary = DarkBackground,
    secondary = EmeraldSecondary,
    background = DarkBackground,
    onBackground = DarkTextPrimary,
    surface = DarkSurface,
    onSurface = DarkTextPrimary,
    onSurfaceVariant = DarkTextSecondary,
    outline = DarkOutline,
    error = SemanticError
)

private val LightColors = lightColorScheme(
    primary = EmeraldPrimary,
    onPrimary = LightSurface,
    secondary = EmeraldSecondary,
    background = LightBackground,
    onBackground = LightTextPrimary,
    surface = LightSurface,
    onSurface = LightTextPrimary,
    onSurfaceVariant = LightTextSecondary,
    outline = LightOutline,
    error = SemanticError
)

@Composable
fun StrideTheme(
    appTheme: AppTheme = AppTheme.SYSTEM,
    content: @Composable () -> Unit
) {
    val useDark = when (appTheme) {
        AppTheme.SYSTEM -> isSystemInDarkTheme()
        AppTheme.LIGHT -> false
        AppTheme.DARK -> true
    }
    MaterialTheme(
        colorScheme = if (useDark) DarkColors else LightColors,
        typography = StrideTypography,
        content = content
    )
}
""",

    "app/src/main/java/com/stride/app/ui/components/StepRing.kt": """package com.stride.app.ui.components

import androidx.compose.animation.core.FastOutSlowInEasing
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.animateIntAsState
import androidx.compose.animation.core.tween
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.size
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import com.stride.app.ui.theme.EmeraldPrimary
import com.stride.app.ui.theme.EmeraldSecondary
import java.text.NumberFormat
import java.util.Locale

@Composable
fun StepRing(
    steps: Int,
    goal: Int,
    modifier: Modifier = Modifier,
    ringSize: Dp = 248.dp,
    strokeWidth: Dp = 18.dp
) {
    val targetProgress = if (goal > 0) (steps.toFloat() / goal).coerceIn(0f, 1f) else 0f
    val animatedProgress by animateFloatAsState(
        targetValue = targetProgress,
        animationSpec = tween(durationMillis = 280, easing = FastOutSlowInEasing),
        label = "ringProgress"
    )
    val animatedSteps by animateIntAsState(
        targetValue = steps,
        animationSpec = tween(durationMillis = 250, easing = FastOutSlowInEasing),
        label = "stepCountUp"
    )

    val trackColor = MaterialTheme.colorScheme.outline
    val ringBrush = Brush.sweepGradient(
        listOf(EmeraldPrimary, EmeraldSecondary, EmeraldPrimary)
    )

    val formattedSteps = NumberFormat.getIntegerInstance(Locale.getDefault()).format(animatedSteps)
    val formattedGoal = NumberFormat.getIntegerInstance(Locale.getDefault()).format(goal)

    Box(
        modifier = modifier
            .size(ringSize)
            .semantics {
                contentDescription = "$steps of $goal daily steps"
            },
        contentAlignment = Alignment.Center
    ) {
        Canvas(modifier = Modifier.size(ringSize)) {
            val strokePx = strokeWidth.toPx()
            drawArc(
                color = trackColor,
                startAngle = -90f,
                sweepAngle = 360f,
                useCenter = false,
                style = Stroke(width = strokePx, cap = StrokeCap.Round)
            )
            if (animatedProgress > 0.001f) {
                drawArc(
                    brush = ringBrush,
                    startAngle = -90f,
                    sweepAngle = 360f * animatedProgress,
                    useCenter = false,
                    style = Stroke(width = strokePx, cap = StrokeCap.Round)
                )
            }
        }

        Column(
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center
        ) {
            Text(
                text = "STEPS TODAY",
                style = MaterialTheme.typography.labelSmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
            Spacer(modifier = Modifier.height(4.dp))
            Text(
                text = formattedSteps,
                style = MaterialTheme.typography.displayLarge,
                color = MaterialTheme.colorScheme.onBackground
            )
            Spacer(modifier = Modifier.height(4.dp))
            Text(
                text = "GOAL $formattedGoal",
                style = MaterialTheme.typography.labelSmall,
                color = EmeraldPrimary
            )
        }
    }
}
""",

    "app/src/main/java/com/stride/app/ui/components/StatTile.kt": """package com.stride.app.ui.components

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

@Composable
fun StatTile(
    label: String,
    value: String,
    unit: String,
    modifier: Modifier = Modifier
) {
    Surface(
        modifier = modifier,
        shape = RoundedCornerShape(18.dp),
        color = MaterialTheme.colorScheme.surface,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outline)
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 14.dp, vertical = 14.dp)
        ) {
            Text(
                text = label.uppercase(),
                style = MaterialTheme.typography.labelSmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
            Spacer(modifier = Modifier.height(8.dp))
            Text(
                text = value,
                style = MaterialTheme.typography.headlineMedium,
                color = MaterialTheme.colorScheme.onSurface
            )
            Spacer(modifier = Modifier.height(2.dp))
            Text(
                text = unit,
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
    }
}
""",

    "app/src/main/java/com/stride/app/ui/components/BarChart.kt": """package com.stride.app.ui.components

import androidx.compose.foundation.Canvas
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import com.stride.app.ui.theme.EmeraldPrimary

@Composable
fun BarChart(
    bars: List<Pair<String, Int>>,
    modifier: Modifier = Modifier,
    chartHeight: Dp = 136.dp
) {
    val maxVal = (bars.maxOfOrNull { it.second } ?: 1).coerceAtLeast(100)
    val trackColor = MaterialTheme.colorScheme.outline

    Column(modifier = modifier.fillMaxWidth()) {
        Canvas(
            modifier = Modifier
                .fillMaxWidth()
                .height(chartHeight)
        ) {
            if (bars.isEmpty()) return@Canvas
            val count = bars.size
            val slotWidth = size.width / count
            val barWidth = (slotWidth * 0.56f).coerceIn(6f, 36f)

            bars.forEachIndexed { index, (_, value) ->
                val x = index * slotWidth + (slotWidth - barWidth) / 2f
                drawRoundRect(
                    color = trackColor.copy(alpha = 0.45f),
                    topLeft = Offset(x, 0f),
                    size = Size(barWidth, size.height),
                    cornerRadius = CornerRadius(barWidth / 2f, barWidth / 2f)
                )
                val ratio = (value.toFloat() / maxVal).coerceIn(0f, 1f)
                val barHeight = (size.height * ratio).coerceAtLeast(if (value > 0) 6f else 0f)
                if (barHeight > 0f) {
                    drawRoundRect(
                        color = EmeraldPrimary,
                        topLeft = Offset(x, size.height - barHeight),
                        size = Size(barWidth, barHeight),
                        cornerRadius = CornerRadius(barWidth / 2f, barWidth / 2f)
                    )
                }
            }
        }
        Spacer(modifier = Modifier.height(8.dp))
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            val step = (bars.size / 5).coerceAtLeast(1)
            bars.forEachIndexed { idx, (label, _) ->
                if (idx % step == 0 || idx == bars.lastIndex) {
                    Text(
                        text = label,
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
            }
        }
    }
}
""",

    "app/src/main/java/com/stride/app/ui/components/RouteMapView.kt": """package com.stride.app.ui.components

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.StrokeJoin
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.unit.dp
import com.google.android.gms.maps.CameraUpdateFactory
import com.google.android.gms.maps.model.CameraPosition
import com.google.android.gms.maps.model.LatLng
import com.google.maps.android.compose.GoogleMap
import com.google.maps.android.compose.MapUiSettings
import com.google.maps.android.compose.Polyline
import com.google.maps.android.compose.rememberCameraPositionState
import com.stride.app.BuildConfig
import com.stride.app.domain.model.LatLngPoint
import com.stride.app.ui.theme.EmeraldPrimary

@Composable
fun RouteMapView(
    points: List<LatLngPoint>,
    modifier: Modifier = Modifier
) {
    val hasMapsApiKey = BuildConfig.MAPS_API_KEY.isNotBlank() &&
        BuildConfig.MAPS_API_KEY != "YOUR_GOOGLE_MAPS_API_KEY_HERE"

    Surface(
        modifier = modifier,
        shape = RoundedCornerShape(20.dp),
        color = MaterialTheme.colorScheme.surface,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outline)
    ) {
        if (hasMapsApiKey && points.isNotEmpty()) {
            val latLngList = points.map { LatLng(it.latitude, it.longitude) }
            val last = latLngList.last()
            val cameraPositionState = rememberCameraPositionState {
                position = CameraPosition.fromLatLngZoom(last, 16f)
            }
            LaunchedEffect(last) {
                cameraPositionState.animate(CameraUpdateFactory.newLatLngZoom(last, 16f))
            }
            GoogleMap(
                modifier = Modifier.fillMaxSize(),
                cameraPositionState = cameraPositionState,
                uiSettings = MapUiSettings(
                    zoomControlsEnabled = false,
                    mapToolbarEnabled = false,
                    compassEnabled = false
                )
            ) {
                Polyline(
                    points = latLngList,
                    color = EmeraldPrimary,
                    width = 12f
                )
            }
        } else {
            CanvasVectorRouteFallback(points = points)
        }
    }
}

@Composable
private fun CanvasVectorRouteFallback(points: List<LatLngPoint>) {
    val gridColor = MaterialTheme.colorScheme.outline.copy(alpha = 0.5f)
    val labelColor = MaterialTheme.colorScheme.onSurfaceVariant

    Box(modifier = Modifier.fillMaxSize()) {
        Canvas(
            modifier = Modifier
                .fillMaxSize()
                .padding(24.dp)
        ) {
            val stepX = size.width / 6f
            val stepY = size.height / 4f
            for (i in 1..5) {
                drawLine(
                    color = gridColor,
                    start = Offset(i * stepX, 0f),
                    end = Offset(i * stepX, size.height),
                    strokeWidth = 1f
                )
            }
            for (j in 1..3) {
                drawLine(
                    color = gridColor,
                    start = Offset(0f, j * stepY),
                    end = Offset(size.width, j * stepY),
                    strokeWidth = 1f
                )
            }

            if (points.size >= 2) {
                val minLat = points.minOf { it.latitude }
                val maxLat = points.maxOf { it.latitude }
                val minLng = points.minOf { it.longitude }
                val maxLng = points.maxOf { it.longitude }
                val latSpan = (maxLat - minLat).coerceAtLeast(0.0002)
                val lngSpan = (maxLng - minLng).coerceAtLeast(0.0002)

                val path = Path()
                points.forEachIndexed { idx, pt ->
                    val x = (((pt.longitude - minLng) / lngSpan) * size.width).toFloat()
                    val y = (size.height - ((pt.latitude - minLat) / latSpan) * size.height).toFloat()
                    if (idx == 0) path.moveTo(x, y) else path.lineTo(x, y)
                }

                drawPath(
                    path = path,
                    color = EmeraldPrimary,
                    style = Stroke(width = 8f, cap = StrokeCap.Round, join = StrokeJoin.Round)
                )

                val first = points.first()
                val last = points.last()
                val startOffset = Offset(
                    (((first.longitude - minLng) / lngSpan) * size.width).toFloat(),
                    (size.height - ((first.latitude - minLat) / latSpan) * size.height).toFloat()
                )
                val endOffset = Offset(
                    (((last.longitude - minLng) / lngSpan) * size.width).toFloat(),
                    (size.height - ((last.latitude - minLat) / latSpan) * size.height).toFloat()
                )
                drawCircle(color = EmeraldPrimary.copy(alpha = 0.4f), radius = 14f, center = endOffset)
                drawCircle(color = EmeraldPrimary, radius = 7f, center = startOffset)
                drawCircle(color = EmeraldPrimary, radius = 8f, center = endOffset)
            }
        }

        if (points.isEmpty()) {
            Text(
                text = "GPS ROUTE TRACE READY",
                style = MaterialTheme.typography.labelSmall,
                color = labelColor,
                modifier = Alignment.Center.let { Modifier.align(it) }
            )
        }
    }
}
""",

    "app/src/main/java/com/stride/app/ui/screens/onboarding/OnboardingScreen.kt": """package com.stride.app.ui.screens.onboarding

import android.Manifest
import android.os.Build
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Slider
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableFloatStateOf
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import com.stride.app.ui.theme.EmeraldPrimary
import kotlin.math.roundToInt

@Composable
fun OnboardingScreen(
    onCompleteOnboarding: (heightCm: Int, weightKg: Float, goal: Int) -> Unit
) {
    var step by remember { mutableIntStateOf(0) }
    var heightText by remember { mutableStateOf("172") }
    var weightText by remember { mutableStateOf("70") }
    var goalSlider by remember { mutableFloatStateOf(10000f) }
    var permissionsRequested by remember { mutableStateOf(false) }

    val permissionLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.RequestMultiplePermissions()
    ) {
        permissionsRequested = true
    }

    Surface(
        modifier = Modifier.fillMaxSize(),
        color = MaterialTheme.colorScheme.background
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(24.dp),
            verticalArrangement = Arrangement.SpaceBetween
        ) {
            Column {
                Spacer(modifier = Modifier.height(32.dp))
                Text(
                    text = "STEP ${step + 1} OF 3",
                    style = MaterialTheme.typography.labelSmall,
                    color = EmeraldPrimary
                )
                Spacer(modifier = Modifier.height(12.dp))

                when (step) {
                    0 -> {
                        Text(
                            text = "Precision step & route tracking.",
                            style = MaterialTheme.typography.displayMedium,
                            color = MaterialTheme.colorScheme.onBackground
                        )
                        Spacer(modifier = Modifier.height(16.dp))
                        Text(
                            text = "Stride fuses your hardware pedometer, 3D gyroscope, accelerometer, and Kalman-smoothed GPS for trustworthy metrics—without accounts, ads, or cloud tracking.",
                            style = MaterialTheme.typography.bodyLarge,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }

                    1 -> {
                        Text(
                            text = "Calibrate your stride & goal.",
                            style = MaterialTheme.typography.headlineMedium,
                            color = MaterialTheme.colorScheme.onBackground
                        )
                        Spacer(modifier = Modifier.height(8.dp))
                        Text(
                            text = "Used strictly on-device to estimate initial stride length and calorie burn.",
                            style = MaterialTheme.typography.bodyMedium,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                        Spacer(modifier = Modifier.height(24.dp))
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.spacedBy(12.dp)
                        ) {
                            OutlinedTextField(
                                value = heightText,
                                onValueChange = { heightText = it.filter { c -> c.isDigit() } },
                                label = { Text("Height (cm)") },
                                keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                                modifier = Modifier.weight(1f)
                            )
                            OutlinedTextField(
                                value = weightText,
                                onValueChange = { weightText = it.filter { c -> c.isDigit() || c == '.' } },
                                label = { Text("Weight (kg)") },
                                keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Decimal),
                                modifier = Modifier.weight(1f)
                            )
                        }
                        Spacer(modifier = Modifier.height(28.dp))
                        Text(
                            text = "DAILY STEP GOAL: ${goalSlider.roundToInt()}",
                            style = MaterialTheme.typography.labelSmall,
                            color = EmeraldPrimary
                        )
                        Slider(
                            value = goalSlider,
                            onValueChange = { goalSlider = (it / 500f).roundToInt() * 500f },
                            valueRange = 3000f..25000f
                        )
                    }

                    2 -> {
                        Text(
                            text = "Permissions with purpose.",
                            style = MaterialTheme.typography.headlineMedium,
                            color = MaterialTheme.colorScheme.onBackground
                        )
                        Spacer(modifier = Modifier.height(16.dp))
                        PermissionCard(
                            title = "Motion & Activity Recognition",
                            rationale = "Counts your steps all day and pauses counting when you are driving."
                        )
                        Spacer(modifier = Modifier.height(12.dp))
                        PermissionCard(
                            title = "Fine Location (Optional)",
                            rationale = "Used only during active Walk/Run/Hike sessions to map your route and calibrate stride length. Stride still works with steps-only if denied."
                        )
                        Spacer(modifier = Modifier.height(12.dp))
                        PermissionCard(
                            title = "Notifications",
                            rationale = "Displays live workout controls and alerts you once per day when you hit your step goal."
                        )
                        Spacer(modifier = Modifier.height(20.dp))
                        OutlinedButton(
                            onClick = {
                                val perms = buildList {
                                    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
                                        add(Manifest.permission.ACTIVITY_RECOGNITION)
                                    }
                                    add(Manifest.permission.ACCESS_FINE_LOCATION)
                                    add(Manifest.permission.ACCESS_COARSE_LOCATION)
                                    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
                                        add(Manifest.permission.POST_NOTIFICATIONS)
                                    }
                                }
                                permissionLauncher.launch(perms.toTypedArray())
                            },
                            modifier = Modifier.fillMaxWidth().height(52.dp),
                            shape = RoundedCornerShape(16.dp)
                        ) {
                            Text(if (permissionsRequested) "Permissions Configured ✓" else "Grant Sensor & Location Permissions")
                        }
                    }
                }
            }

            Button(
                onClick = {
                    if (step < 2) {
                        step++
                    } else {
                        val h = heightText.toIntOrNull()?.coerceIn(100, 240) ?: 172
                        val w = weightText.toFloatOrNull()?.coerceIn(30f, 250f) ?: 70f
                        onCompleteOnboarding(h, w, goalSlider.roundToInt())
                    }
                },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(54.dp),
                shape = RoundedCornerShape(16.dp),
                colors = ButtonDefaults.buttonColors(containerColor = EmeraldPrimary)
            ) {
                Text(
                    text = if (step < 2) "Continue" else "Enter Stride",
                    style = MaterialTheme.typography.titleMedium
                )
            }
        }
    }
}

@Composable
private fun PermissionCard(title: String, rationale: String) {
    Surface(
        shape = RoundedCornerShape(16.dp),
        color = MaterialTheme.colorScheme.surface,
        border = BorderStroke(1.dp, MaterialTheme.colorScheme.outline),
        modifier = Modifier.fillMaxWidth()
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(text = title, style = MaterialTheme.typography.titleMedium)
            Spacer(modifier = Modifier.height(4.dp))
            Text(
                text = rationale,
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
    }
}
""",

    "app/src/main/java/com/stride/app/ui/screens/today/TodayViewModel.kt": """package com.stride.app.ui.screens.today

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.stride.app.data.repository.StrideRepository
import com.stride.app.domain.model.DailySummary
import com.stride.app.domain.model.UnitSystem
import com.stride.app.domain.model.UserProfile
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.combine
import kotlinx.coroutines.flow.stateIn
import java.time.LocalDate
import javax.inject.Inject

data class TodayUiState(
    val summary: DailySummary = DailySummary(
        dateEpochDay = LocalDate.now().toEpochDay(),
        steps = 0,
        goal = 10000,
        distanceMeters = 0.0,
        caloriesKcal = 0,
        activeMinutes = 0
    ),
    val unitSystem: UnitSystem = UnitSystem.METRIC
)

@HiltViewModel
class TodayViewModel @Inject constructor(
    repository: StrideRepository
) : ViewModel() {

    val uiState: StateFlow<TodayUiState> = combine(
        repository.observeTodaySummary(),
        repository.userProfileFlow
    ) { summary, profile: UserProfile ->
        TodayUiState(
            summary = summary.copy(goal = profile.dailyGoal),
            unitSystem = profile.unitSystem
        )
    }.stateIn(
        scope = viewModelScope,
        started = SharingStarted.WhileSubscribed(5000),
        initialValue = TodayUiState()
    )
}
""",

    "app/src/main/java/com/stride/app/ui/screens/today/TodayScreen.kt": """package com.stride.app.ui.screens.today

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.PlayArrow
import androidx.compose.material3.ExtendedFloatingActionButton
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.stride.app.domain.model.UnitSystem
import com.stride.app.ui.components.BarChart
import com.stride.app.ui.components.StatTile
import com.stride.app.ui.components.StepRing
import com.stride.app.ui.theme.EmeraldPrimary
import java.time.LocalDate
import java.time.format.DateTimeFormatter

@Composable
fun TodayScreen(
    onStartActivityClick: () -> Unit,
    viewModel: TodayViewModel = hiltViewModel()
) {
    val state by viewModel.uiState.collectAsStateWithLifecycle()
    val summary = state.summary

    val distValue = if (state.unitSystem == UnitSystem.METRIC) {
        "%.2f".format(summary.distanceMeters / 1000.0)
    } else {
        "%.2f".format(summary.distanceMeters / 1609.34)
    }
    val distUnit = if (state.unitSystem == UnitSystem.METRIC) "km" else "mi"

    Scaffold(
        floatingActionButton = {
            ExtendedFloatingActionButton(
                onClick = onStartActivityClick,
                containerColor = EmeraldPrimary,
                contentColor = MaterialTheme.colorScheme.onPrimary,
                icon = { Icon(Icons.Outlined.PlayArrow, contentDescription = "Start Activity") },
                text = { Text("Start Activity") }
            )
        }
    ) { innerPadding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
                .verticalScroll(rememberScrollState())
                .padding(horizontal = 20.dp, vertical = 16.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Column {
                    Text(
                        text = LocalDate.now().format(DateTimeFormatter.ofPattern("EEEE, MMM d")).uppercase(),
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                    Text(
                        text = "Today",
                        style = MaterialTheme.typography.headlineMedium,
                        color = MaterialTheme.colorScheme.onBackground
                    )
                }
            }

            Spacer(modifier = Modifier.height(24.dp))

            Box(contentAlignment = Alignment.Center) {
                StepRing(steps = summary.steps, goal = summary.goal)
            }

            Spacer(modifier = Modifier.height(28.dp))

            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(10.dp)
            ) {
                StatTile(
                    label = "Distance",
                    value = distValue,
                    unit = distUnit,
                    modifier = Modifier.weight(1f)
                )
                StatTile(
                    label = "Calories",
                    value = summary.caloriesKcal.toString(),
                    unit = "kcal",
                    modifier = Modifier.weight(1f)
                )
                StatTile(
                    label = "Active",
                    value = summary.activeMinutes.toString(),
                    unit = "min",
                    modifier = Modifier.weight(1f)
                )
            }

            Spacer(modifier = Modifier.height(20.dp))

            Surface(
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(20.dp),
                color = MaterialTheme.colorScheme.surface,
                border = BorderStroke(1.dp, MaterialTheme.colorScheme.outline)
            ) {
                Column(modifier = Modifier.padding(18.dp)) {
                    Text(
                        text = "HOURLY DISTRIBUTION",
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                    Spacer(modifier = Modifier.height(14.dp))
                    val hourlyBars = summary.hourlySteps.mapIndexed { hr, count ->
                        val label = when (hr) {
                            0 -> "12a"
                            6 -> "6a"
                            12 -> "12p"
                            18 -> "6p"
                            23 -> "11p"
                            else -> "$hr"
                        }
                        label to count
                    }
                    BarChart(bars = hourlyBars)
                }
            }

            Spacer(modifier = Modifier.height(80.dp))
        }
    }
}
""",

    "app/src/main/java/com/stride/app/ui/screens/activity/ActivityViewModel.kt": """package com.stride.app.ui.screens.activity

import android.content.Context
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.stride.app.data.repository.StrideRepository
import com.stride.app.domain.model.ActivityType
import com.stride.app.domain.model.LiveSessionState
import com.stride.app.service.TrackingService
import dagger.hilt.android.lifecycle.HiltViewModel
import dagger.hilt.android.qualifiers.ApplicationContext
import kotlinx.coroutines.flow.MutableSharedFlow
import kotlinx.coroutines.flow.SharedFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asSharedFlow
import kotlinx.coroutines.launch
import javax.inject.Inject

@HiltViewModel
class ActivityViewModel @Inject constructor(
    @ApplicationContext private val appContext: Context,
    private val repository: StrideRepository
) : ViewModel() {

    val liveSession: StateFlow<LiveSessionState> = repository.liveSession

    private val _sessionFinishedEvent = MutableSharedFlow<Long>()
    val sessionFinishedEvent: SharedFlow<Long> = _sessionFinishedEvent.asSharedFlow()

    fun startSession(type: ActivityType) {
        TrackingService.startSession(appContext, type)
    }

    fun pauseSession() {
        TrackingService.sendCommand(appContext, TrackingService.ACTION_PAUSE_SESSION)
    }

    fun resumeSession() {
        TrackingService.sendCommand(appContext, TrackingService.ACTION_RESUME_SESSION)
    }

    fun stopSession() {
        viewModelScope.launch {
            val savedId = repository.stopAndSaveSession()
            TrackingService.sendCommand(appContext, TrackingService.ACTION_STOP_SESSION)
            if (savedId != null) {
                _sessionFinishedEvent.emit(savedId)
            }
        }
    }
}
""",

    "app/src/main/java/com/stride/app/ui/screens/activity/ActivityScreen.kt": """package com.stride.app.ui.screens.activity

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.FilterChip
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.stride.app.domain.model.ActivityType
import com.stride.app.ui.components.RouteMapView
import com.stride.app.ui.components.StatTile
import com.stride.app.ui.theme.EmeraldPrimary
import com.stride.app.ui.theme.SemanticError

@Composable
fun ActivityScreen(
    onNavigateToSummary: (Long) -> Unit,
    viewModel: ActivityViewModel = hiltViewModel()
) {
    val session by viewModel.liveSession.collectAsStateWithLifecycle()
    var selectedType by remember { mutableStateOf(ActivityType.WALK) }

    LaunchedEffect(Unit) {
        viewModel.sessionFinishedEvent.collect { sessionId ->
            onNavigateToSummary(sessionId)
        }
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
            .padding(20.dp)
    ) {
        Text(
            text = "GPS & SENSOR FUSION",
            style = MaterialTheme.typography.labelSmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
        Text(
            text = if (session.isActive) "${session.type.label} Session" else "Activity Session",
            style = MaterialTheme.typography.headlineMedium,
            color = MaterialTheme.colorScheme.onBackground
        )

        Spacer(modifier = Modifier.height(14.dp))

        if (!session.isActive) {
            Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                ActivityType.entries.forEach { type ->
                    FilterChip(
                        selected = selectedType == type,
                        onClick = { selectedType = type },
                        label = { Text(type.label) }
                    )
                }
            }
            Spacer(modifier = Modifier.height(14.dp))
        }

        RouteMapView(
            points = session.route,
            modifier = Modifier
                .fillMaxWidth()
                .height(230.dp)
        )

        Spacer(modifier = Modifier.height(18.dp))

        val mins = session.durationSeconds / 60
        val secs = session.durationSeconds % 60
        val durationFormatted = "%02d:%02d".format(mins, secs)

        val paceMin = session.currentPaceSecPerKm / 60
        val paceSec = session.currentPaceSecPerKm % 60
        val paceFormatted = if (session.currentPaceSecPerKm > 0) "%d'%02d\\"".format(paceMin, paceSec) else "--'--\\""

        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(10.dp)
        ) {
            StatTile(
                label = "Duration",
                value = durationFormatted,
                unit = "mm:ss",
                modifier = Modifier.weight(1f)
            )
            StatTile(
                label = "Distance",
                value = "%.2f".format(session.distanceMeters / 1000.0),
                unit = "km",
                modifier = Modifier.weight(1f)
            )
            StatTile(
                label = "Steps",
                value = session.steps.toString(),
                unit = "steps",
                modifier = Modifier.weight(1f)
            )
        }

        Spacer(modifier = Modifier.height(10.dp))

        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(10.dp)
        ) {
            StatTile(
                label = "Pace",
                value = paceFormatted,
                unit = "/km",
                modifier = Modifier.weight(1f)
            )
            StatTile(
                label = "Speed",
                value = "%.1f".format(session.currentSpeedMps * 3.6),
                unit = "km/h",
                modifier = Modifier.weight(1f)
            )
            StatTile(
                label = "Cadence",
                value = session.cadenceSpm.toString(),
                unit = "spm",
                modifier = Modifier.weight(1f)
            )
        }

        Spacer(modifier = Modifier.height(24.dp))

        if (!session.isActive) {
            Button(
                onClick = { viewModel.startSession(selectedType) },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(54.dp),
                shape = RoundedCornerShape(16.dp),
                colors = ButtonDefaults.buttonColors(containerColor = EmeraldPrimary)
            ) {
                Text("Start ${selectedType.label}", style = MaterialTheme.typography.titleMedium)
            }
        } else {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                OutlinedButton(
                    onClick = {
                        if (session.isPaused) viewModel.resumeSession() else viewModel.pauseSession()
                    },
                    modifier = Modifier
                        .weight(1f)
                        .height(54.dp),
                    shape = RoundedCornerShape(16.dp),
                    border = BorderStroke(1.dp, EmeraldPrimary)
                ) {
                    Text(if (session.isPaused) "Resume" else "Pause")
                }

                Button(
                    onClick = { viewModel.stopSession() },
                    modifier = Modifier
                        .weight(1f)
                        .height(54.dp),
                    shape = RoundedCornerShape(16.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = SemanticError)
                ) {
                    Text("Finish")
                }
            }
        }
    }
}
""",

    "app/src/main/java/com/stride/app/ui/screens/history/HistoryViewModel.kt": """package com.stride.app.ui.screens.history

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.stride.app.data.repository.StrideRepository
import com.stride.app.domain.model.ActivitySession
import com.stride.app.domain.model.DailySummary
import com.stride.app.domain.model.HistoryInsights
import com.stride.app.domain.model.HistoryRange
import com.stride.app.domain.usecase.CalculateStatsUseCase
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.combine
import kotlinx.coroutines.flow.stateIn
import java.time.LocalDate
import java.time.format.DateTimeFormatter
import javax.inject.Inject

data class HistoryUiState(
    val range: HistoryRange = HistoryRange.WEEK,
    val insights: HistoryInsights = HistoryInsights(0, 0, 0, 0.0, emptyList(), emptyList()),
    val sessions: List<ActivitySession> = emptyList()
)

@HiltViewModel
class HistoryViewModel @Inject constructor(
    repository: StrideRepository,
    private val statsUseCase: CalculateStatsUseCase
) : ViewModel() {

    private val selectedRange = MutableStateFlow(HistoryRange.WEEK)

    val uiState: StateFlow<HistoryUiState> = combine(
        selectedRange,
        repository.observeAllDays(),
        repository.observeAllSessions()
    ) { range, days, sessions ->
        val today = LocalDate.now()
        val bars = buildBarsForRange(range, days, today)
        val insights = statsUseCase.buildInsights(
            days = days,
            sessions = sessions,
            chartBars = bars,
            todayEpochDay = today.toEpochDay()
        )
        HistoryUiState(
            range = range,
            insights = insights,
            sessions = sessions
        )
    }.stateIn(
        scope = viewModelScope,
        started = SharingStarted.WhileSubscribed(5000),
        initialValue = HistoryUiState()
    )

    fun selectRange(range: HistoryRange) {
        selectedRange.value = range
    }

    private fun buildBarsForRange(
        range: HistoryRange,
        days: List<DailySummary>,
        today: LocalDate
    ): List<Pair<String, Int>> {
        val byDay = days.associateBy { it.dateEpochDay }
        return when (range) {
            HistoryRange.DAY -> {
                val todaySummary = byDay[today.toEpochDay()]
                val hourly = todaySummary?.hourlySteps ?: List(24) { 0 }
                hourly.mapIndexed { hr, steps -> "${hr}h" to steps }
            }
            HistoryRange.WEEK -> {
                val fmt = DateTimeFormatter.ofPattern("EEE")
                (6 downTo 0).map { offset ->
                    val d = today.minusDays(offset.toLong())
                    d.format(fmt) to (byDay[d.toEpochDay()]?.steps ?: 0)
                }
            }
            HistoryRange.MONTH -> {
                (29 downTo 0).map { offset ->
                    val d = today.minusDays(offset.toLong())
                    d.dayOfMonth.toString() to (byDay[d.toEpochDay()]?.steps ?: 0)
                }
            }
            HistoryRange.YEAR -> {
                val fmt = DateTimeFormatter.ofPattern("MMM")
                (11 downTo 0).map { monthOffset ->
                    val ym = today.minusMonths(monthOffset.toLong())
                    val monthTotal = days.filter {
                        val ld = LocalDate.ofEpochDay(it.dateEpochDay)
                        ld.year == ym.year && ld.month == ym.month
                    }.sumOf { it.steps }
                    ym.format(fmt) to monthTotal
                }
            }
        }
    }
}
""",

    "app/src/main/java/com/stride/app/ui/screens/history/HistoryScreen.kt": """package com.stride.app.ui.screens.history

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.FilterChip
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.stride.app.domain.model.HistoryRange
import com.stride.app.ui.components.BarChart
import com.stride.app.ui.components.StatTile
import com.stride.app.ui.theme.EmeraldPrimary
import java.time.Instant
import java.time.ZoneId
import java.time.format.DateTimeFormatter

@Composable
fun HistoryScreen(
    onSessionClick: (Long) -> Unit,
    viewModel: HistoryViewModel = hiltViewModel()
) {
    val state by viewModel.uiState.collectAsStateWithLifecycle()
    val insights = state.insights

    LazyColumn(
        modifier = Modifier
            .fillMaxSize()
            .padding(horizontal = 20.dp, vertical = 16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        item {
            Text(
                text = "INSIGHTS & TRENDS",
                style = MaterialTheme.typography.labelSmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
            Text(
                text = "History",
                style = MaterialTheme.typography.headlineMedium,
                color = MaterialTheme.colorScheme.onBackground
            )
        }

        item {
            Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                HistoryRange.entries.forEach { range ->
                    FilterChip(
                        selected = state.range == range,
                        onClick = { viewModel.selectRange(range) },
                        label = { Text(range.label) }
                    )
                }
            }
        }

        item {
            Surface(
                shape = RoundedCornerShape(20.dp),
                color = MaterialTheme.colorScheme.surface,
                border = BorderStroke(1.dp, MaterialTheme.colorScheme.outline),
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(modifier = Modifier.padding(18.dp)) {
                    Text(
                        text = "${state.range.label.uppercase()} STEP VOLUME",
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                    Spacer(modifier = Modifier.height(14.dp))
                    BarChart(bars = insights.chartBars)
                }
            }
        }

        item {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(10.dp)
            ) {
                StatTile(
                    label = "Daily Avg",
                    value = insights.averageSteps.toString(),
                    unit = "steps",
                    modifier = Modifier.weight(1f)
                )
                StatTile(
                    label = "Best Day",
                    value = insights.bestDaySteps.toString(),
                    unit = "steps",
                    modifier = Modifier.weight(1f)
                )
            }
            Spacer(modifier = Modifier.height(10.dp))
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(10.dp)
            ) {
                StatTile(
                    label = "Streak",
                    value = insights.currentStreakDays.toString(),
                    unit = "days",
                    modifier = Modifier.weight(1f)
                )
                StatTile(
                    label = "Total Dist",
                    value = "%.1f".format(insights.totalDistanceKm),
                    unit = "km",
                    modifier = Modifier.weight(1f)
                )
            }
        }

        item {
            Text(
                text = "ACHIEVEMENTS",
                style = MaterialTheme.typography.labelSmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
            Spacer(modifier = Modifier.height(8.dp))
            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                insights.badges.forEach { badge ->
                    Surface(
                        shape = RoundedCornerShape(16.dp),
                        color = MaterialTheme.colorScheme.surface,
                        border = BorderStroke(
                            1.dp,
                            if (badge.unlocked) EmeraldPrimary else MaterialTheme.colorScheme.outline
                        ),
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Row(
                            modifier = Modifier.padding(14.dp),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Column {
                                Text(text = badge.title, style = MaterialTheme.typography.titleMedium)
                                Text(
                                    text = badge.description,
                                    style = MaterialTheme.typography.bodyMedium,
                                    color = MaterialTheme.colorScheme.onSurfaceVariant
                                )
                            }
                            Text(
                                text = if (badge.unlocked) "UNLOCKED" else "LOCKED",
                                style = MaterialTheme.typography.labelSmall,
                                color = if (badge.unlocked) EmeraldPrimary else MaterialTheme.colorScheme.onSurfaceVariant
                            )
                        }
                    }
                }
            }
        }

        item {
            Text(
                text = "PAST SESSIONS",
                style = MaterialTheme.typography.labelSmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }

        if (state.sessions.isEmpty()) {
            item {
                Text(
                    text = "No recorded walks or runs yet.",
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
        } else {
            items(state.sessions, key = { it.id }) { session ->
                val dateStr = Instant.ofEpochMilli(session.startTimeMs)
                    .atZone(ZoneId.systemDefault())
                    .format(DateTimeFormatter.ofPattern("MMM d, HH:mm"))
                Surface(
                    shape = RoundedCornerShape(16.dp),
                    color = MaterialTheme.colorScheme.surface,
                    border = BorderStroke(1.dp, MaterialTheme.colorScheme.outline),
                    modifier = Modifier
                        .fillMaxWidth()
                        .clickable { onSessionClick(session.id) }
                ) {
                    Row(
                        modifier = Modifier.padding(16.dp),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Column {
                            Text(
                                text = "${session.type.label} • $dateStr",
                                style = MaterialTheme.typography.titleMedium
                            )
                            Text(
                                text = "${session.steps} steps • ${session.durationSeconds / 60} min",
                                style = MaterialTheme.typography.bodyMedium,
                                color = MaterialTheme.colorScheme.onSurfaceVariant
                            )
                        }
                        Text(
                            text = "%.2f km".format(session.distanceMeters / 1000.0),
                            style = MaterialTheme.typography.titleMedium,
                            color = EmeraldPrimary
                        )
                    }
                }
            }
        }
    }
}
""",

    "app/src/main/java/com/stride/app/ui/screens/summary/SessionSummaryViewModel.kt": """package com.stride.app.ui.screens.summary

import androidx.lifecycle.SavedStateHandle
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.stride.app.data.repository.StrideRepository
import com.stride.app.domain.model.ActivitySession
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import javax.inject.Inject

@HiltViewModel
class SessionSummaryViewModel @Inject constructor(
    savedStateHandle: SavedStateHandle,
    private val repository: StrideRepository
) : ViewModel() {

    private val _session = MutableStateFlow<ActivitySession?>(null)
    val session: StateFlow<ActivitySession?> = _session.asStateFlow()

    init {
        val id = savedStateHandle.get<Long>("sessionId") ?: -1L
        if (id != -1L) {
            viewModelScope.launch {
                _session.value = repository.getSessionById(id)
            }
        }
    }
}
""",

    "app/src/main/java/com/stride/app/ui/screens/summary/SessionSummaryScreen.kt": """package com.stride.app.ui.screens.summary

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.stride.app.ui.components.BarChart
import com.stride.app.ui.components.RouteMapView
import com.stride.app.ui.components.StatTile

@Composable
fun SessionSummaryScreen(
    onBack: () -> Unit,
    viewModel: SessionSummaryViewModel = hiltViewModel()
) {
    val session by viewModel.session.collectAsStateWithLifecycle()

    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
            .padding(20.dp)
    ) {
        Text(
            text = "SESSION SUMMARY",
            style = MaterialTheme.typography.labelSmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
        Text(
            text = session?.type?.label ?: "Workout",
            style = MaterialTheme.typography.headlineMedium,
            color = MaterialTheme.colorScheme.onBackground
        )

        Spacer(modifier = Modifier.height(16.dp))

        val s = session
        if (s != null) {
            RouteMapView(
                points = s.routePoints,
                modifier = Modifier
                    .fillMaxWidth()
                    .height(220.dp)
            )

            Spacer(modifier = Modifier.height(16.dp))

            val paceMin = s.avgPaceSecPerKm / 60
            val paceSec = s.avgPaceSecPerKm % 60
            val paceStr = if (s.avgPaceSecPerKm > 0) "%d'%02d\\"".format(paceMin, paceSec) else "--'--\\""

            Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                StatTile(
                    label = "Distance",
                    value = "%.2f".format(s.distanceMeters / 1000.0),
                    unit = "km",
                    modifier = Modifier.weight(1f)
                )
                StatTile(
                    label = "Duration",
                    value = "%02d:%02d".format(s.durationSeconds / 60, s.durationSeconds % 60),
                    unit = "mm:ss",
                    modifier = Modifier.weight(1f)
                )
                StatTile(
                    label = "Steps",
                    value = s.steps.toString(),
                    unit = "steps",
                    modifier = Modifier.weight(1f)
                )
            }

            Spacer(modifier = Modifier.height(10.dp))

            Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                StatTile(
                    label = "Avg Pace",
                    value = paceStr,
                    unit = "/km",
                    modifier = Modifier.weight(1f)
                )
                StatTile(
                    label = "Calories",
                    value = s.caloriesKcal.toString(),
                    unit = "kcal",
                    modifier = Modifier.weight(1f)
                )
                StatTile(
                    label = "Cadence",
                    value = s.avgCadenceSpm.toString(),
                    unit = "spm",
                    modifier = Modifier.weight(1f)
                )
            }

            Spacer(modifier = Modifier.height(18.dp))

            Surface(
                shape = RoundedCornerShape(20.dp),
                color = MaterialTheme.colorScheme.surface,
                border = BorderStroke(1.dp, MaterialTheme.colorScheme.outline),
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(modifier = Modifier.padding(18.dp)) {
                    Text(
                        text = "PACE SPLITS (SEC / KM)",
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                    Spacer(modifier = Modifier.height(12.dp))
                    val splitBars = s.paceSplitsSecPerKm.mapIndexed { index, sec ->
                        "#${index + 1}" to sec
                    }
                    BarChart(bars = splitBars)
                }
            }
        }

        Spacer(modifier = Modifier.height(24.dp))
        OutlinedButton(
            onClick = onBack,
            modifier = Modifier
                .fillMaxWidth()
                .height(50.dp),
            shape = RoundedCornerShape(16.dp)
        ) {
            Text("Done")
        }
    }
}
""",

    "app/src/main/java/com/stride/app/ui/screens/profile/ProfileViewModel.kt": """package com.stride.app.ui.screens.profile

import android.content.Context
import android.content.Intent
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.stride.app.data.datastore.UserPreferencesRepository
import com.stride.app.data.repository.StrideRepository
import com.stride.app.domain.model.AppTheme
import com.stride.app.domain.model.BiologicalSex
import com.stride.app.domain.model.UnitSystem
import com.stride.app.domain.model.UserProfile
import com.stride.app.domain.usecase.ExportCsvUseCase
import com.stride.app.service.TrackingService
import dagger.hilt.android.lifecycle.HiltViewModel
import dagger.hilt.android.qualifiers.ApplicationContext
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch
import javax.inject.Inject

@HiltViewModel
class ProfileViewModel @Inject constructor(
    @ApplicationContext private val context: Context,
    private val prefs: UserPreferencesRepository,
    private val repository: StrideRepository,
    private val exportCsvUseCase: ExportCsvUseCase
) : ViewModel() {

    val profile: StateFlow<UserProfile> = prefs.userProfileFlow.stateIn(
        scope = viewModelScope,
        started = SharingStarted.WhileSubscribed(5000),
        initialValue = UserProfile()
    )

    fun updateGoal(newGoal: Int) {
        viewModelScope.launch {
            prefs.updateProfile { it.copy(dailyGoal = newGoal.coerceIn(1000, 50000)) }
        }
    }

    fun updateBodyMetrics(heightCm: Int, weightKg: Float, age: Int, sex: BiologicalSex) {
        viewModelScope.launch {
            prefs.updateProfile {
                it.copy(heightCm = heightCm, weightKg = weightKg, age = age, sex = sex)
            }
        }
    }

    fun updateUnits(unitSystem: UnitSystem) {
        viewModelScope.launch {
            prefs.updateProfile { it.copy(unitSystem = unitSystem) }
        }
    }

    fun updateTheme(theme: AppTheme) {
        viewModelScope.launch {
            prefs.updateProfile { it.copy(theme = theme) }
        }
    }

    fun toggleGps(enabled: Boolean) {
        viewModelScope.launch {
            prefs.updateProfile { it.copy(gpsEnabled = enabled) }
        }
    }

    fun toggleBackgroundTracking(enabled: Boolean) {
        viewModelScope.launch {
            prefs.updateProfile { it.copy(backgroundTrackingEnabled = enabled) }
            if (enabled) {
                TrackingService.startPassive(context)
            }
        }
    }

    fun exportDataCsv() {
        viewModelScope.launch {
            val days = repository.getAllDaysSnapshot()
            val sessions = repository.getAllSessionsSnapshot()
            val uri = exportCsvUseCase.exportToCsvUri(days, sessions)
            val shareIntent = Intent(Intent.ACTION_SEND).apply {
                type = "text/csv"
                putExtra(Intent.EXTRA_STREAM, uri)
                addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION or Intent.FLAG_ACTIVITY_NEW_TASK)
            }
            context.startActivity(
                Intent.createChooser(shareIntent, "Export Stride CSV").apply {
                    addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                }
            )
        }
    }

    fun deleteAllData() {
        viewModelScope.launch {
            repository.deleteAllData()
        }
    }
}
""",

    "app/src/main/java/com/stride/app/ui/screens/profile/ProfileScreen.kt": """package com.stride.app.ui.screens.profile

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.FilterChip
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Slider
import androidx.compose.material3.Surface
import androidx.compose.material3.Switch
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.stride.app.domain.model.AppTheme
import com.stride.app.domain.model.UnitSystem
import com.stride.app.ui.theme.EmeraldPrimary
import com.stride.app.ui.theme.SemanticError
import kotlin.math.roundToInt

@Composable
fun ProfileScreen(
    viewModel: ProfileViewModel = hiltViewModel()
) {
    val profile by viewModel.profile.collectAsStateWithLifecycle()

    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
            .padding(20.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        Column {
            Text(
                text = "CALIBRATION & PRIVACY",
                style = MaterialTheme.typography.labelSmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
            Text(
                text = "Profile & Settings",
                style = MaterialTheme.typography.headlineMedium,
                color = MaterialTheme.colorScheme.onBackground
            )
        }

        Surface(
            shape = RoundedCornerShape(18.dp),
            color = MaterialTheme.colorScheme.surface,
            border = BorderStroke(1.dp, MaterialTheme.colorScheme.outline),
            modifier = Modifier.fillMaxWidth()
        ) {
            Column(modifier = Modifier.padding(16.dp)) {
                Text(
                    text = "DAILY GOAL: ${profile.dailyGoal} STEPS",
                    style = MaterialTheme.typography.labelSmall,
                    color = EmeraldPrimary
                )
                Slider(
                    value = profile.dailyGoal.toFloat(),
                    onValueChange = { viewModel.updateGoal((it / 500f).roundToInt() * 500) },
                    valueRange = 3000f..25000f
                )
                Text(
                    text = "Calibrated Stride Length: ${"%.2f".format(profile.effectiveStrideMeters)} m (${profile.heightCm} cm, ${profile.weightKg.roundToInt()} kg)",
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
        }

        Surface(
            shape = RoundedCornerShape(18.dp),
            color = MaterialTheme.colorScheme.surface,
            border = BorderStroke(1.dp, MaterialTheme.colorScheme.outline),
            modifier = Modifier.fillMaxWidth()
        ) {
            Column(modifier = Modifier.padding(16.dp)) {
                Text(
                    text = "UNITS",
                    style = MaterialTheme.typography.labelSmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    UnitSystem.entries.forEach { unit ->
                        FilterChip(
                            selected = profile.unitSystem == unit,
                            onClick = { viewModel.updateUnits(unit) },
                            label = { Text(unit.name) }
                        )
                    }
                }
                Spacer(modifier = Modifier.height(10.dp))
                Text(
                    text = "APPEARANCE",
                    style = MaterialTheme.typography.labelSmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    AppTheme.entries.forEach { t ->
                        FilterChip(
                            selected = profile.theme == t,
                            onClick = { viewModel.updateTheme(t) },
                            label = { Text(t.name) }
                        )
                    }
                }
            }
        }

        Surface(
            shape = RoundedCornerShape(18.dp),
            color = MaterialTheme.colorScheme.surface,
            border = BorderStroke(1.dp, MaterialTheme.colorScheme.outline),
            modifier = Modifier.fillMaxWidth()
        ) {
            Column(modifier = Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Column(modifier = Modifier.weight(1f)) {
                        Text("GPS Route & Stride Calibration", style = MaterialTheme.typography.titleMedium)
                        Text(
                            "Active only during Walk/Run sessions",
                            style = MaterialTheme.typography.bodyMedium,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                    Switch(checked = profile.gpsEnabled, onCheckedChange = viewModel::toggleGps)
                }

                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Column(modifier = Modifier.weight(1f)) {
                        Text("All-Day Background Counting", style = MaterialTheme.typography.titleMedium)
                        Text(
                            "Uses low-power hardware batching",
                            style = MaterialTheme.typography.bodyMedium,
                            color = MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }
                    Switch(
                        checked = profile.backgroundTrackingEnabled,
                        onCheckedChange = viewModel::toggleBackgroundTracking
                    )
                }
            }
        }

        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            OutlinedButton(
                onClick = viewModel::exportDataCsv,
                modifier = Modifier
                    .weight(1f)
                    .height(50.dp),
                shape = RoundedCornerShape(14.dp)
            ) {
                Text("Export CSV")
            }
            Button(
                onClick = viewModel::deleteAllData,
                modifier = Modifier
                    .weight(1f)
                    .height(50.dp),
                shape = RoundedCornerShape(14.dp),
                colors = ButtonDefaults.buttonColors(containerColor = SemanticError)
            ) {
                Text("Delete All Data")
            }
        }

        Surface(
            shape = RoundedCornerShape(16.dp),
            color = MaterialTheme.colorScheme.surface,
            border = BorderStroke(1.dp, MaterialTheme.colorScheme.outline),
            modifier = Modifier.fillMaxWidth()
        ) {
            Column(modifier = Modifier.padding(16.dp)) {
                Text(
                    text = "ON-DEVICE PRIVACY GUARANTEE",
                    style = MaterialTheme.typography.labelSmall,
                    color = EmeraldPrimary
                )
                Spacer(modifier = Modifier.height(4.dp))
                Text(
                    text = "100% of your steps, routes, and body metrics stay inside your device's local Room database. Stride contains zero analytics SDKs, zero accounts, and makes no network requests except map tiles when enabled.",
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }
        }
    }
}
""",

    "app/src/main/java/com/stride/app/ui/navigation/StrideNavHost.kt": """package com.stride.app.ui.navigation

import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.core.tween
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.DirectionsRun
import androidx.compose.material.icons.outlined.Insights
import androidx.compose.material.icons.outlined.PersonOutline
import androidx.compose.material.icons.outlined.Today
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.navigation.NavGraph.Companion.findStartDestination
import androidx.navigation.NavType
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController
import androidx.navigation.navArgument
import com.stride.app.ui.screens.activity.ActivityScreen
import com.stride.app.ui.screens.history.HistoryScreen
import com.stride.app.ui.screens.profile.ProfileScreen
import com.stride.app.ui.screens.summary.SessionSummaryScreen
import com.stride.app.ui.screens.today.TodayScreen

sealed class BottomTab(val route: String, val label: String, val icon: ImageVector) {
    data object Today : BottomTab("today", "Today", Icons.Outlined.Today)
    data object Activity : BottomTab("activity", "Activity", Icons.Outlined.DirectionsRun)
    data object History : BottomTab("history", "History", Icons.Outlined.Insights)
    data object Profile : BottomTab("profile", "Profile", Icons.Outlined.PersonOutline)
}

@Composable
fun StrideNavHost() {
    val navController = rememberNavController()
    val tabs = listOf(BottomTab.Today, BottomTab.Activity, BottomTab.History, BottomTab.Profile)
    val navBackStackEntry by navController.currentBackStackEntryAsState()
    val currentRoute = navBackStackEntry?.destination?.route

    Scaffold(
        bottomBar = {
            NavigationBar(
                containerColor = MaterialTheme.colorScheme.surface
            ) {
                tabs.forEach { tab ->
                    NavigationBarItem(
                        selected = currentRoute == tab.route,
                        onClick = {
                            navController.navigate(tab.route) {
                                popUpTo(navController.graph.findStartDestination().id) {
                                    saveState = true
                                }
                                launchSingleTop = true
                                restoreState = true
                            }
                        },
                        icon = { Icon(tab.icon, contentDescription = tab.label) },
                        label = { Text(tab.label) }
                    )
                }
            }
        }
    ) { innerPadding ->
        NavHost(
            navController = navController,
            startDestination = BottomTab.Today.route,
            modifier = Modifier.padding(innerPadding),
            enterTransition = { fadeIn(animationSpec = tween(220)) },
            exitTransition = { fadeOut(animationSpec = tween(220)) }
        ) {
            composable(BottomTab.Today.route) {
                TodayScreen(
                    onStartActivityClick = {
                        navController.navigate(BottomTab.Activity.route)
                    }
                )
            }
            composable(BottomTab.Activity.route) {
                ActivityScreen(
                    onNavigateToSummary = { sessionId ->
                        navController.navigate("summary/$sessionId")
                    }
                )
            }
            composable(BottomTab.History.route) {
                HistoryScreen(
                    onSessionClick = { sessionId ->
                        navController.navigate("summary/$sessionId")
                    }
                )
            }
            composable(BottomTab.Profile.route) {
                ProfileScreen()
            }
            composable(
                route = "summary/{sessionId}",
                arguments = listOf(navArgument("sessionId") { type = NavType.LongType })
            ) {
                SessionSummaryScreen(onBack = { navController.popBackStack() })
            }
        }
    }
}
""",

    "app/src/main/java/com/stride/app/StrideApp.kt": """package com.stride.app

import android.app.Application
import androidx.hilt.work.HiltWorkerFactory
import androidx.work.Configuration
import com.stride.app.service.DailyRolloverWorker
import dagger.hilt.android.HiltAndroidApp
import javax.inject.Inject

@HiltAndroidApp
class StrideApp : Application(), Configuration.Provider {

    @Inject lateinit var workerFactory: HiltWorkerFactory

    override val workManagerConfiguration: Configuration
        get() = Configuration.Builder()
            .setWorkerFactory(workerFactory)
            .build()

    override fun onCreate() {
        super.onCreate()
        DailyRolloverWorker.schedule(this)
    }
}
""",

    "app/src/main/java/com/stride/app/MainActivity.kt": """package com.stride.app

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.runtime.getValue
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.lifecycleScope
import com.stride.app.data.datastore.UserPreferencesRepository
import com.stride.app.domain.model.UserProfile
import com.stride.app.service.TrackingService
import com.stride.app.ui.navigation.StrideNavHost
import com.stride.app.ui.screens.onboarding.OnboardingScreen
import com.stride.app.ui.theme.StrideTheme
import dagger.hilt.android.AndroidEntryPoint
import kotlinx.coroutines.launch
import javax.inject.Inject

@AndroidEntryPoint
class MainActivity : ComponentActivity() {

    @Inject lateinit var prefs: UserPreferencesRepository

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            val profile by prefs.userProfileFlow.collectAsStateWithLifecycle(
                initialValue = UserProfile(onboardingCompleted = true)
            )

            StrideTheme(appTheme = profile.theme) {
                if (!profile.onboardingCompleted) {
                    OnboardingScreen(
                        onCompleteOnboarding = { heightCm, weightKg, goal ->
                            lifecycleScope.launch {
                                prefs.updateProfile {
                                    it.copy(
                                        heightCm = heightCm,
                                        weightKg = weightKg,
                                        dailyGoal = goal,
                                        calibratedStrideMeters = heightCm * 0.00415,
                                        onboardingCompleted = true
                                    )
                                }
                                TrackingService.startPassive(this@MainActivity)
                            }
                        }
                    )
                } else {
                    StrideNavHost()
                }
            }
        }
    }
}
"""
}


def main():
    root = Path("stride")
    for rel_path, content in FILES.items():
        file_path = root / rel_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")
    print(f"Created Stride project with {len(FILES)} files inside './stride/'")
    print("Next step: Push the './stride' folder to GitHub and download your APK from the 'Actions' tab!")


if __name__ == "__main__":
    main()
