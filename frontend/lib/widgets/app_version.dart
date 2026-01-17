import 'package:flutter/material.dart';

class AppVersion extends StatelessWidget {
  const AppVersion({super.key});

  // Injected at build time via --dart-define
  static const String _version =
      String.fromEnvironment('APP_VERSION', defaultValue: 'unknown');

  @override
  Widget build(BuildContext context) {
    return Text(
      'Version: v$_version',
      style: Theme.of(context)
          .textTheme
          .bodySmall
          ?.copyWith(color: Colors.grey),
    );
  }
}

