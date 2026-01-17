class AppConfig {
  static const String appVersion =
      String.fromEnvironment('APP_VERSION', defaultValue: 'unknown');
}
