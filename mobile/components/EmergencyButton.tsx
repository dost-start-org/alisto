import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import type { StackNavigationProp } from '@react-navigation/stack';
import type { RootStackParamList } from '../navigation/AppNavigator';

type EmergencyButtonNavProp = StackNavigationProp<
  RootStackParamList,
  'UserHome'
>;

export default function EmergencyButton() {
  const navigation = useNavigation<EmergencyButtonNavProp>();

  return (
    <View style={styles.wrapper}>
      <View style={[styles.shadowCircle, styles.circleLarge]} />
      <View style={[styles.shadowCircle, styles.circleMedium]} />

      <TouchableOpacity
        style={styles.circleMain}
        onPress={() => navigation.navigate('EmergencyOptions')}
      >
        <Text style={styles.text}>Press to{"\n"}Report Emergency</Text>
      </TouchableOpacity>
    </View>
  );
}

const BASE_SIZE = 200;

const styles = StyleSheet.create({
  wrapper: {
    justifyContent: 'center',
    alignItems: 'center',
    position: 'relative',
    marginVertical: 30,
  },

  circleLarge: {
    width: BASE_SIZE * 1.6,
    height: BASE_SIZE * 1.6,
    backgroundColor: '#F3D8D8',
    borderRadius: (BASE_SIZE * 1.6) / 2,
  },

  circleMedium: {
    width: BASE_SIZE * 1.3,
    height: BASE_SIZE * 1.3,
    backgroundColor: '#F9BEBE',
    borderRadius: (BASE_SIZE * 1.3) / 2,
  },

  circleMain: {
    width: BASE_SIZE,
    height: BASE_SIZE,
    borderRadius: BASE_SIZE / 2,
    backgroundColor: '#E63C3C',
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingVertical: 10,
    elevation: 8,
    zIndex: 3,
  },

  text: {
    color: '#fff',
    fontSize: 24,
    fontFamily: 'Poppins-Medium',
    textAlign: 'center',
    lineHeight: 30,
  },

  shadowCircle: {
    position: 'absolute',
    zIndex: 1,
  },
});