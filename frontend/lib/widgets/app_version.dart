import 'package:flutter/material.dart';

class AppVersion extends StatelessWidget {
  const AppVersion({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    // Read the version passed via --dart-define during CI/CD build
    const version = String.fromEnvironment('APP_VERSION', defaultValue: 'unknown');

    return Text(
      'Version: v$version',
      style: Theme.of(context)
          .textTheme
          .bodySmall
          ?.copyWith(color: Colors.grey),
    );
  }
}
