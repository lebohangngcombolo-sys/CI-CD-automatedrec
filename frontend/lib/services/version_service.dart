import 'dart:convert';
import 'package:http/http.dart' as http;
import '../utils/api_endpoints.dart';

class VersionService {
  static Future<String> fetchBackendVersion() async {
    try {
      final response = await http.get(
        Uri.parse(ApiEndpoints.appVersion),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return data['version'] ?? 'unknown';
      }
      return 'unknown';
    } catch (_) {
      return 'unknown';
    }
  }
}
