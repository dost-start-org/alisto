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
  ScrollView,
  KeyboardAvoidingView,
  TouchableWithoutFeedback,
  Platform,
  Linking,
} from 'react-native';
import { useRouter, useLocalSearchParams } from 'expo-router';
import * as Location from 'expo-location';
import { useFonts } from 'expo-font';
import WaveBackground from '../components/WaveBackground';
import ConfirmReport from '../components/ConfirmReport';
import TopNavBar from '../components/TopNavBar';

const { width } = Dimensions.get('window');
const MIN_LOCATION_LENGTH = 5;

export default function LocationSelect() {
  const router = useRouter();
  const params = useLocalSearchParams();
  const emergencyData = JSON.parse(params.emergencyData as string);

  const [fontsLoaded] = useFonts({
    'Poppins-Medium': require('../assets/fonts/Poppins-Medium.ttf'),
  });

  const navTitle = `Reporting ${emergencyData.title}`;

  const [location, setLocation] = useState('');
  const [description, setDescription] = useState('');
  const [modalVisible, setModalVisible] = useState(false);
  const [warningMessage, setWarningMessage] = useState('');

  const handleSendLocation = async () => {
  Keyboard.dismiss();
  setWarningMessage('');

  let servicesEnabled = await Location.hasServicesEnabledAsync();
  if (!servicesEnabled) {
    setWarningMessage('Location services are disabled. Please turn them on in your device settings.');
    await Linking.openSettings();
    return;
  }

  let { status } = await Location.requestForegroundPermissionsAsync();
    if (status !== 'granted') {
      setWarningMessage('Permission to access location was denied');
      return;
    }

    setWarningMessage('Getting current location...');

    try {
      let currentLocation = await Location.getLastKnownPositionAsync();

      if (!currentLocation) {
        currentLocation = await Promise.race([
          Location.getCurrentPositionAsync({
            accuracy: Location.Accuracy.Lowest,
          }),
          new Promise<never>((_, reject) => setTimeout(() => reject(new Error('Location timeout')), 5000)),
        ]);
      }

      if (currentLocation && currentLocation.coords) {
        const formattedLocation = `${currentLocation.coords.latitude.toFixed(6)}, ${currentLocation.coords.longitude.toFixed(6)}`;
        setLocation(formattedLocation);
        setWarningMessage('');
      } else {
        setWarningMessage('Could not retrieve coordinates. Try again.');
      }
    } catch (error) {
      console.error('Location error:', error);
      setWarningMessage('Could not get location. Check device settings or enter manually.');
    }
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
    router.push({
      pathname: '/ReportingEmergency',
      params: {
        emergencyData: JSON.stringify(emergencyData),
        location: location,
        description: description,
      },
    });
  };

  const handleAddImage = () => {
    console.log('Add Image button pressed');
  };

  if (!fontsLoaded) {
    return null;
  }

  return (
    <View style={styles.container}>
      <WaveBackground />
      <TopNavBar title={navTitle} theme="red" />
      <KeyboardAvoidingView behavior={Platform.OS === 'ios' ? 'padding' : 'height'} style={{ flex: 1 }}>
        <TouchableWithoutFeedback onPress={Keyboard.dismiss}>
          <ScrollView contentContainerStyle={styles.content}>
            <Text style={styles.title}>Location of Incident</Text>
            <View style={styles.sectionContainer}>
              <TouchableOpacity style={[styles.buttonBase, styles.blackButton]} onPress={handleSendLocation}>
                <Image source={require('../assets/locationicon.png')} style={styles.mainbuttonIcon} />
                <Text style={styles.mainButtonText}>Open Location Services</Text>
              </TouchableOpacity>
              <Text style={styles.orText}>or</Text>
              <Text style={styles.smallText}>If you’re not in location</Text>
              <TextInput
                style={[
                  styles.textInput,
                  styles.locationInput,
                  warningMessage !== '' && styles.inputError,
                ]}
                placeholder="Exact location of incident or Landmarks"
                placeholderTextColor="#999"
                value={location}
                onChangeText={(text) => {
                  setLocation(text);
                  if (warningMessage !== '') setWarningMessage('');
                }}
              />
              {warningMessage !== '' && <Text style={styles.warningText}>{warningMessage}</Text>}
            </View>

            <Text style={styles.sectionTitle}>Description of the Incident (Optional)</Text>
            <Text style={styles.sectionSubtitle}>What exactly happened?</Text>

            <View style={styles.sectionContainer}>
              <TextInput
                style={[styles.textInput, styles.descriptionInput]}
                placeholder="Share more information that help responders to understand the incident."
                placeholderTextColor="#999"
                value={description}
                onChangeText={setDescription}
                multiline
              />
              <View style={styles.addImageButtonContainer}>
                <TouchableOpacity style={[styles.buttonBase, styles.blackButton]} onPress={handleAddImage}>
                  <Image source={require('../assets/addimage.png')} style={styles.buttonIcon} />
                  <Text style={styles.buttonText}>Add Image</Text>
                </TouchableOpacity>
              </View>
            </View>

            <TouchableOpacity
              style={[styles.buttonBase, styles.blueButton, styles.submitButton]}
              onPress={handleSubmit}
            >
              <Image source={require('../assets/submiticon.png')} style={styles.buttonIcon} />
              <Text style={styles.buttonText}>Submit</Text>
            </TouchableOpacity>
          </ScrollView>
        </TouchableWithoutFeedback>
      </KeyboardAvoidingView>

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
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#fff' },
  content: {
    flexGrow: 1,
    alignItems: 'center',
    paddingTop: 80,
    paddingHorizontal: 20,
    paddingBottom: 30,
  },
  title: {
    fontFamily: 'Poppins-Medium',
    fontSize: 24,
    color: '#fff',
    textAlign: 'center',
    marginTop: 10,
    marginBottom: 15,
    textShadowColor: 'rgba(0,0,0,0.3)',
    textShadowOffset: { width: 1, height: 1 },
    textShadowRadius: 3,
  },
  sectionContainer: {
    width: width * 0.9,
    backgroundColor: 'rgba(255, 255, 255, 0.15)',
    borderRadius: 10,
    padding: 15,
    marginBottom: 20,
    alignItems: 'center',
  },
  buttonBase: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 4,
    paddingHorizontal: 10,
    borderRadius: 8,
    elevation: 3,
    justifyContent: 'center',
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
  mainButtonText: {
    fontFamily: 'Poppins-Medium',
    color: '#fff',
    fontSize: 16,
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
  orText: {
    fontFamily: 'Poppins-Medium',
    fontSize: 16,
    color: '#fff',
    marginVertical: 8,
    textAlign: 'center',
  },
  smallText: {
    fontFamily: 'Poppins-Medium',
    fontSize: 16,
    color: '#fff',
    marginBottom: 8,
    textAlign: 'center',
  },
  textInput: {
    fontFamily: 'Poppins-Medium',
    width: '100%',
    backgroundColor: '#f9f9f9',
    borderRadius: 10,
    paddingHorizontal: 12,
    paddingTop: 12,
    paddingBottom: 12,
    fontSize: 16,
    color: '#000',
    borderWidth: 1,
    borderColor: '#ddd',
    elevation: 2,
    textAlignVertical: 'top',
  },
  locationInput: {
    height: 70,
  },
  descriptionInput: {
    height: 120,
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
  sectionTitle: {
    fontFamily: 'Poppins-Medium',
    fontSize: 18,
    color: '#fff',
    textAlign: 'center',
    marginBottom: 5,
    textShadowColor: 'rgba(0,0,0,0.3)',
    textShadowOffset: { width: 1, height: 1 },
    textShadowRadius: 3,
  },
  sectionSubtitle: {
    fontFamily: 'Poppins-Medium',
    fontStyle: 'italic',
    fontSize: 14,
    color: '#eee',
    textAlign: 'center',
    marginBottom: 8,
  },
  addImageButtonContainer: {
    width: '100%',
    alignItems: 'flex-end',
    marginTop: 8,
  },
  submitButton: {
    marginTop: 15,
  },
  dimOverlay: {
    ...StyleSheet.absoluteFillObject,
    backgroundColor: 'rgba(0, 0, 0, 0.4)',
    zIndex: 51,
  },
  modalContainer: {
    ...StyleSheet.absoluteFillObject,
    justifyContent: 'center',
    alignItems: 'center',
    zIndex: 52,
  },
});
