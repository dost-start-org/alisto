import React from 'react';
import { View, TouchableOpacity, StyleSheet, Image } from 'react-native';
import { useRouter } from 'expo-router';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

export default function TopNav() {
  const router = useRouter();
  const insets = useSafeAreaInsets();

  return (
    <View style={[styles.container, { paddingTop: insets.top }]}>
      <View style={styles.inner}>
        <View style={styles.logoContainer}>
          <Image
            source={require('../assets/alistologoquezoncity.png')}
            style={styles.logo}
          />
        </View>

        <TouchableOpacity
          onPress={() => router.push('/Notifications')}
          style={styles.menuButton}
          activeOpacity={0.6}
        >
          <Image
            source={require('../assets/notifications.png')}
            style={styles.notificationIcon}
          />
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: '#f2f2f2',
    elevation: 3,
    shadowColor: '#000',
    shadowOpacity: 0.1,
    shadowRadius: 3,
    shadowOffset: { width: 0, height: 2 },
  },
  inner: {
    height: 60,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 16,
  },
  logoContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginLeft: -24,
  },
  logo: {
    width: 140,
    height: 40,
    resizeMode: 'contain',
  },
  menuButton: {
    padding: 8,
  },
  notificationIcon: {
    width: 40,
    height: 40,
    resizeMode: 'contain',
  },
});