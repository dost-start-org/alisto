import React from 'react';
import { View, TouchableOpacity, Text, StyleSheet, Image } from 'react-native';

type Props = {
  onNavigate?: (screen: string) => void;
};

export default function BottomNav({ onNavigate }: Props) {
  return (
    <View style={styles.bottomNav}>
      <TouchableOpacity
        style={styles.bottomButton}
        onPress={() => onNavigate?.('UserHome')}
      >
        <Image source={require('../assets/homeicon.png')} style={styles.icon} />
        <Text style={styles.bottomText}>Home</Text>
      </TouchableOpacity>

      <TouchableOpacity
        style={styles.bottomButton}
        onPress={() => onNavigate?.('Hotlines')}
      >
        <Image source={require('../assets/hotlinesicon.png')} style={styles.icon} />
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
    height: 70,
    flexDirection: 'row',
    borderTopWidth: 1,
    borderColor: '#ccc',
    backgroundColor: '#f2f2f2',
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
