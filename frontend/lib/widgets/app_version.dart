import 'package:flutter/material.dart';
import '../services/version_service.dart';

class AppVersion extends StatefulWidget {
  const AppVersion({super.key});

  @override
  State<AppVersion> createState() => _AppVersionState();
}

class _AppVersionState extends State<AppVersion> {
  String version = '...';

  @override
  void initState() {
    super.initState();
    VersionService.fetchBackendVersion().then((v) {
      if (mounted) {
        setState(() => version = v);
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Text(
      'Version: v$version',
      style:
          Theme.of(context).textTheme.bodySmall?.copyWith(color: Colors.grey),
    );
  }
}
