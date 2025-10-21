import React from 'react';
import { View, TouchableOpacity, Text, StyleSheet, Image } from 'react-native';

export type NavScreen = 'UserHome' | 'Hotlines';

type Props = {
  onNavigate?: (screen: NavScreen) => void;
};

export default function BottomNav({ onNavigate }: Props) {
  return (
    <View style={styles.bottomNav}>
      <TouchableOpacity
        style={styles.bottomButton}
        onPress={() => onNavigate?.('UserHome')}
      >
        <Image
          source={require('../assets/homeicon.png')}
          style={styles.icon}
        />
        <Text style={styles.bottomText}>Home</Text>
      </TouchableOpacity>

      <TouchableOpacity
        style={styles.bottomButton}
        onPress={() => onNavigate?.('Hotlines')}
      >
        <Image
          source={require('../assets/hotlinesicon.png')}
          style={styles.icon}
        />
        <Text style={styles.bottomText}>Hotlines</Text>
      </TouchableOpacity>

      <View style={styles.bottomButton}>
        <Image source={require('../assets/profile.png')} style={styles.icon} />
        <Text style={styles.bottomText}>Profile</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  bottomNav: {
    height: 84,
    flexDirection: 'row',
    backgroundColor: '#fff',
    borderTopLeftRadius: 20,
    borderTopRightRadius: 20,
    elevation: 10,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: -3 },
    shadowOpacity: 0.1,
    shadowRadius: 5,
  },
  bottomButton: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  icon: {
    width: 24,
    height: 24,
    marginBottom: 4,
    resizeMode: 'contain',
  },
  bottomText: {
    fontSize: 14,
    fontWeight: '600',
    color: '#E83737',
    fontFamily: 'Inter',
  },
});