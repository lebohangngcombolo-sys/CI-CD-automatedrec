import 'package:flutter/material.dart';

class AppVersion extends StatelessWidget {
  const AppVersion({super.key});

  static const String _version = String.fromEnvironment(
    'APP_VERSION',
    defaultValue: 'unknown',
  );

  @override
  Widget build(BuildContext context) {
    final isDev = _version.contains('_DEV');
    final isStaging = _version.contains('_STAGING');

    final color = isDev
        ? Colors.orange
        : isStaging
        ? Colors.blue
        : Colors.green;

    return Text(
      'Version: v$_version',
      style: const TextStyle(fontSize: 12).copyWith(color: color),
    );
  }
}
