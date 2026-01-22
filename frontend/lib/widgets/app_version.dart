import 'package:flutter/material.dart';

class AppVersion extends StatelessWidget {
  const AppVersion({super.key});

  // Calendar version (date + env)
  static const String calver = String.fromEnvironment(
    'APP_VERSION',
    defaultValue: 'unknown',
  );

  // Semantic version
  static const String semver = String.fromEnvironment(
    'APP_SEMVER',
    defaultValue: '0.0.0',
  );

  @override
  Widget build(BuildContext context) {
    final isDev = calver.contains('_DEV');
    final isStaging = calver.contains('_STAGING');

    final color = isDev
        ? Colors.orange
        : isStaging
        ? Colors.blue
        : Colors.green;

    return Text(
      'Version: v$semver ($calver)',
      style: const TextStyle(fontSize: 12).copyWith(color: color),
    );
  }
}
