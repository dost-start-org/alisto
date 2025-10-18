import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Image,
  TextInput,
  Dimensions,
  Keyboard,
} from 'react-native';
import { useNavigation, useRoute, RouteProp } from '@react-navigation/native';
import type { StackNavigationProp } from '@react-navigation/stack';
import type { RootStackParamList } from '../navigation/AppNavigator';
import WaveBackground from '../components/WaveBackground';
import ConfirmReport from '../components/ConfirmReport';
import TopNavBar from '../components/TopNavBar';

type LocationSelectScreenNavProp = StackNavigationProp<
  RootStackParamList,
  'LocationSelectScreen'
>;

type LocationSelectScreenRouteProp = RouteProp<
  RootStackParamList,
  'LocationSelectScreen'
>;

const { height, width } = Dimensions.get('window');

const MIN_LOCATION_LENGTH = 5;

const generateRandomCoordinates = () => {
  const minLat = 14.4;
  const maxLat = 14.7;
  const minLon = 120.9;
  const maxLon = 121.1;

  const randomLat = (Math.random() * (maxLat - minLat) + minLat).toFixed(6);
  const randomLon = (Math.random() * (maxLon - minLon) + minLon).toFixed(6);

  return `Lat: ${randomLat}, Lon: ${randomLon}`;
};

export default function LocationSelectScreen() {
  const navigation = useNavigation<LocationSelectScreenNavProp>();
  const route = useRoute<LocationSelectScreenRouteProp>();
  const { emergencyData } = route.params;

  const navTitle = `Reporting ${emergencyData.title}`;

  const [location, setLocation] = useState('');
  const [modalVisible, setModalVisible] = useState(false);
  const [warningMessage, setWarningMessage] = useState('');

  const handleSendLocation = () => {
    Keyboard.dismiss();
    const randomLocation = generateRandomCoordinates();
    setLocation(randomLocation);
    setWarningMessage('');
    setModalVisible(true);
  };

  const handleSubmit = () => {
    Keyboard.dismiss();
    const trimmedLocation = location.trim();

    if (trimmedLocation === '') {
      setWarningMessage('Location input is required.');
    } else if (trimmedLocation.length < MIN_LOCATION_LENGTH) {
      setWarningMessage(`Location must be at least ${MIN_LOCATION_LENGTH} characters.`);
    } else {
      setWarningMessage('');
      setModalVisible(true);
    }
  };

  const handleConfirm = () => {
    setModalVisible(false);
    navigation.navigate('ReportingEmergencyScreen', {
      emergencyData,
      location,
    });
  };

  const handleAddImage = () => {
    console.log('Add Image button pressed');
  };

  return (
    <View style={styles.container}>
      <WaveBackground />
      <View style={styles.overlay}>
        <>
          <TopNavBar title={navTitle} theme="red" />
          <View style={styles.content}>
            <Text style={styles.title}>
              Are you in the place{'\n'}of incident?
            </Text>
            <TouchableOpacity
              style={[styles.buttonBase, styles.mainblueButton]}
              onPress={handleSendLocation}
            >
              <Image
                source={require('../assets/locationicon.png')}
                style={styles.mainbuttonIcon}
              />
              <Text style={styles.buttonText}>Send your Location</Text>
            </TouchableOpacity>
            <View style={{ height: height * 0.06 }} />
            <Text style={styles.smallText}>If you’re not in location</Text>
            <TextInput
              style={[
                styles.textInput,
                warningMessage !== '' && styles.inputError,
              ]}
              placeholder="Exact location of incident or Landmarks"
              placeholderTextColor="#999"
              value={location}
              onChangeText={(text) => {
                setLocation(text);
                if (warningMessage !== '') {
                  setWarningMessage('');
                }
              }}
            />
            {warningMessage !== '' && (
              <Text style={styles.warningText}>
                {warningMessage}
              </Text>
            )}
            <View style={{ height: height * 0.04 }} />
            <View style={styles.horizontalButtonContainer}>
              <TouchableOpacity
                style={[styles.buttonBase, styles.blackButton, styles.actionButton]}
                onPress={handleAddImage}
              >
                <Image
                  source={require('../assets/addimage.png')}
                  style={styles.buttonIcon}
                />
                <Text style={styles.buttonText}>Add Image</Text>
              </TouchableOpacity>
              <TouchableOpacity
                style={[styles.buttonBase, styles.blueButton, styles.actionButton]}
                onPress={handleSubmit}
              >
                <Image
                  source={require('../assets/submiticon.png')}
                  style={styles.buttonIcon}
                />
                <Text style={styles.buttonText}>Submit</Text>
              </TouchableOpacity>
            </View>
          </View>
        </>

        {modalVisible && <View style={styles.dimOverlay} />}

        {modalVisible && (
          <View style={styles.modalContainer}>
            <ConfirmReport
              visible={modalVisible}
              onConfirm={handleConfirm}
              onCancel={() => setModalVisible(false)}
            />
          </View>
        )}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#fff' },
  overlay: { flex: 1 },
  content: {
    flex: 1,
    alignItems: 'center',
    paddingTop: 180,
    paddingHorizontal: 20,
  },
  title: {
    fontFamily: 'Poppins-Medium',
    fontSize: 26,
    color: '#fff',
    textAlign: 'center',
    marginBottom: 25,
    textShadowColor: 'rgba(0,0,0,0.3)',
    textShadowOffset: { width: 1, height: 1 },
    textShadowRadius: 3,
  },
  buttonBase: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 7,
    paddingHorizontal: 10,
    borderRadius: 4,
    elevation: 3,
    justifyContent: 'center',
  },
  mainblueButton: {
    backgroundColor: '#007AFF',
    width: '65%',
    paddingVertical: 6,
    paddingHorizontal: 12,
  },
  blueButton: {
    backgroundColor: '#007AFF',
  },
  blackButton: {
    backgroundColor: '#000',
  },
  buttonText: {
    fontFamily: 'Poppins-Medium',
    color: '#fff',
    fontSize: 18,
    marginLeft: 8,
  },
  mainbuttonIcon: {
    width: 32,
    height: 32,
    resizeMode: 'contain',
  },
  buttonIcon: {
    width: 24,
    height: 24,
    resizeMode: 'contain',
  },
  smallText: {
    fontFamily: 'Poppins-Medium',
    fontSize: 16,
    color: '#fff',
    marginBottom: 12,
    textAlign: 'center',
  },
  textInput: {
    fontFamily: 'Poppins-Medium',
    width: width * 0.8,
    height: 70,
    backgroundColor: '#f9f9f9',
    borderRadius: 10,
    paddingHorizontal: 12,
    paddingVertical: 10,
    fontSize: 16,
    color: '#000',
    borderWidth: 1,
    borderColor: '#ddd',
    elevation: 2,
  },
  inputError: {
    borderColor: '#FFEB3B',
    borderWidth: 2,
  },
  warningText: {
    fontFamily: 'Poppins-Medium',
    fontSize: 14,
    color: '#FFEB3B',
    marginTop: 8,
    textAlign: 'center',
    textShadowColor: 'rgba(0,0,0,0.5)',
    textShadowOffset: { width: 1, height: 1 },
    textShadowRadius: 2,
  },
  horizontalButtonContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    width: width * 0.8,
    marginTop: -10,
  },
  actionButton: {
    width: '48%',
  },
  dimOverlay: {
    ...StyleSheet.absoluteFill,
    backgroundColor: 'rgba(0, 0, 0, 0.4)',
    zIndex: 51,
  },
  modalContainer: {
    ...StyleSheet.absoluteFill,
    justifyContent: 'center',
    alignItems: 'center',
    zIndex: 52,
  },
});