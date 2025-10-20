import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Image, Dimensions } from 'react-native';
import { useRouter } from 'expo-router';
import WaveBackground from '../components/WaveBackground';
import TopNavBar from '../components/TopNavBar';

const { height } = Dimensions.get('window');

export default function EmergencyOptions() {
  const router = useRouter();

  const options = [
    { key: 'fire', label: 'Fire', title: 'Fire Incident', icon: require('../assets/fireemergencyicon.png') },
    { key: 'ambulance', label: 'Ambulance', title: 'Medical Emergency', icon: require('../assets/hospitalemergencyicon.png') },
    { key: 'crime', label: 'Crime', title: 'Crime Incident', icon: require('../assets/policeemergencyicon.png') },
    { key: 'disaster', label: 'Disaster', title: 'Disaster Response', icon: require('../assets/disasterresponseemergencyicon.png') },
  ];

  return (
    <View style={styles.container}>
      <WaveBackground />
      <View style={styles.content}>

        <TopNavBar
          showLogo={true}
          theme="light"
        />

        <View style={[styles.middle, { marginTop: height * 0.15 }]}>
          <Text style={styles.title}>
            What is your{'\n'}
            emergency?
          </Text>
          {options.map((opt) => (
            <TouchableOpacity
              key={opt.key}
              style={styles.optionButton}
              onPress={() =>
                router.push({
                  pathname: '/LocationSelect',
                  params: { emergencyData: JSON.stringify(opt) },
                })
              }
            >
              <Text style={styles.optionText}>{opt.label}</Text>
              {opt.icon && <Image source={opt.icon} style={styles.optionIcon} />}
            </TouchableOpacity>
          ))}
        </View>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#fff' },
  content: { flex: 1 },
  middle: {
    flex: 1,
    alignItems: 'center',
    paddingTop: 20,
  },
  title: {
    fontFamily: 'Poppins-Medium',
    fontSize: 28,
    color: '#fff',
    marginBottom: 40,
    textAlign: 'center',
    textShadowColor: 'rgba(0,0,0,0.3)',
    textShadowOffset: { width: 1, height: 1 },
    textShadowRadius: 3,
  },
  optionButton: {
    width: '70%',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    backgroundColor: '#f2f2f2',
    padding: 18,
    marginBottom: 14,
    borderRadius: 12,
    elevation: 2,
  },
  optionText: {
    fontFamily: 'Poppins-Medium',
    fontSize: 18,
    color: '#000',
  },
  optionIcon: {
    width: 50,
    height: 50,
    resizeMode: 'contain',
  },
});