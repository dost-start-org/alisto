import React, { useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Image } from 'react-native';

type CrowdsourceData = {
  id: string;
  emergencyType: string;
  location: string;
  timestamp: string;
};

interface CrowdsourceModalProps {
  onClose: () => void;
  data: CrowdsourceData;
}

export default function CrowdsourceUserScreen({
  onClose,
  data,
}: CrowdsourceModalProps) {
  const { emergencyType, location } = data;
  const [userResponse, setUserResponse] = useState<'initial' | 'yes' | 'no'>(
    'initial'
  );

  return (
    <View style={styles.modalContainer}>
      <Image
        source={require('../assets/crowdsourcequestion.png')}
        style={styles.headerImage}
      />
      <Text style={styles.title}>CROWDSOURCING</Text>

      {userResponse === 'initial' ? (
        <>
          <Text style={styles.question}>
            Did you notice a {emergencyType} incident in your area?
          </Text>
          <Text style={styles.reportIntro}>
            Someone reported a {emergencyType} in
          </Text>
          <View style={styles.addressBox}>
            <Text style={styles.addressText}>{location}</Text>
          </View>

          <View style={styles.buttonContainer}>
            <TouchableOpacity
              style={[styles.button, styles.noButton, styles.flexButton]}
              onPress={() => {
                console.log(`User denied seeing emergency report ${data.id}.`);
                setUserResponse('no');
              }}
            >
              <Text style={styles.buttonText}>No</Text>
            </TouchableOpacity>
            <TouchableOpacity
              style={[styles.button, styles.yesButton, styles.flexButton]}
              onPress={() => {
                console.log(`User confirmed seeing emergency report ${data.id}.`);
                setUserResponse('yes');
              }}
            >
              <Text style={styles.buttonText}>Yes</Text>
            </TouchableOpacity>
          </View>
        </>
      ) : (
        <>
          <Text style={styles.question}>
            {userResponse === 'yes'
              ? 'Thank you for your response.\nHelp is on the way'
              : 'Thanks for cooperating.\nYour response is recorded.'}
          </Text>
          <View style={styles.feedbackButtonContainer}>
            <TouchableOpacity
              style={[styles.button, styles.yesButton, styles.standaloneButton]}
              onPress={onClose}
            >
              <Text style={styles.buttonText}>Close</Text>
            </TouchableOpacity>
          </View>
        </>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  modalContainer: {
    width: '80%',
    backgroundColor: 'white',
    borderRadius: 12,
    paddingVertical: 30,
    paddingHorizontal: 20,
    alignItems: 'center',
    elevation: 10,
    maxWidth: 400,
  },
  headerImage: {
    width: 90,
    height: 90,
    resizeMode: 'contain',
    marginBottom: 10,
  },
  title: {
    fontSize: 13,
    fontWeight: 'bold',
    color: '#2773FF',
    marginBottom: 15,
    fontFamily: 'Poppins-Medium',
  },
  question: {
    fontSize: 16,
    color: 'black',
    textAlign: 'center',
    marginBottom: 8,
    fontFamily: 'Poppins-Medium',
  },
  reportIntro: {
    fontSize: 12,
    color: '#108BFF',
    textAlign: 'center',
    marginBottom: 5,
    fontFamily: 'Poppins-Medium',
  },
  addressBox: {
    width: '100%',
    backgroundColor: '#0F0F0F',
    borderRadius: 8,
    paddingVertical: 8,
    paddingHorizontal: 12,
    marginBottom: 50,
  },
  addressText: {
    fontSize: 11,
    color: 'white',
    textAlign: 'center',
    fontFamily: 'Poppins-Medium',
  },
  buttonContainer: {
    flexDirection: 'row',
    width: '100%',
    justifyContent: 'space-between',
    gap: 10,
  },
  feedbackButtonContainer: {
    width: '100%',
    marginTop: 40,
    alignItems: 'center',
  },
  button: {
    paddingVertical: 10,
    borderRadius: 8,
    alignItems: 'center',
    justifyContent: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 3, height: 3 },
    shadowOpacity: 0.2,
    shadowRadius: 3,
    elevation: 3,
  },
  flexButton: {
    flex: 1,
  },
  standaloneButton: {
    width: '70%',
  },
  noButton: {
    backgroundColor: '#E63C3C',
  },
  yesButton: {
    backgroundColor: '#2773FF',
  },
  buttonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: 'bold',
    fontFamily: 'Poppins-Medium',
  },
});