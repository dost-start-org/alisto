import React from 'react';
import { View, TouchableOpacity, StyleSheet, Image, Text } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

interface TopNavBarProps {
  title?: string;
  showLogo?: boolean;
  theme?: 'light' | 'dark' | 'red';
  isTransparent?: boolean;
}

export default function TopNavBar({
  title,
  showLogo = false,
  theme = 'dark',
  isTransparent = false,
}: TopNavBarProps) {
  const navigation = useNavigation<any>();
  const insets = useSafeAreaInsets();

  const color = theme === 'light' ? '#000' : theme === 'red' ? '#E63C3C' : '#fff';
  const backgroundColor = isTransparent ? 'transparent' : '#fff';
  const position = isTransparent ? 'absolute' : 'relative';

  return (
    <View
      style={[
        styles.container,
        {
          paddingTop: insets.top + 10,
          backgroundColor,
          position,
        },
      ]}
    >
      <TouchableOpacity
        onPress={() => navigation.goBack()}
        style={styles.sideButton}
        activeOpacity={0.6}
        accessibilityLabel="Go back"
      >
        <Image
          source={require('../assets/backicon.png')}
          style={[styles.backIcon, { tintColor: color }]}
        />
      </TouchableOpacity>

      <View style={styles.middleContainer}>
        {showLogo ? (
          <Image
            source={require('../assets/alistologocolored.png')}
            style={styles.logo}
          />
        ) : (
          <Text style={[styles.title, { color }]} numberOfLines={1}>
            {title}
          </Text>
        )}
      </View>

      <View style={styles.sideButton} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    width: '100%',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 16,
    paddingBottom: 10,
    zIndex: 50,
  },
  sideButton: {
    width: 40,
    height: 40,
    justifyContent: 'center',
    alignItems: 'center',
  },
  backIcon: {
    width: 24,
    height: 24,
    resizeMode: 'contain',
  },
  middleContainer: {
    flex: 1,
    alignItems: 'center',
    marginHorizontal: 8,
  },
  title: {
    fontSize: 17,
    fontWeight: '700',
    textAlign: 'center',
  },
  logo: {
    width: 80,
    height: 40,
    resizeMode: 'contain',
  },
});