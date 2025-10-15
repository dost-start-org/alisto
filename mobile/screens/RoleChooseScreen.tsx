import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Image,
} from 'react-native';
import { StackNavigationProp } from '@react-navigation/stack';
import { RootStackParamList } from '../navigation/AppNavigator';

import { useSafeAreaInsets } from 'react-native-safe-area-context';

import GridBackground from '../components/GridBackground';

type RoleChooseScreenNavigationProp = StackNavigationProp<RootStackParamList, 'RoleChoose'>;

interface RoleChooseScreenProps {
  navigation: RoleChooseScreenNavigationProp;
}

const RoleChooseScreen: React.FC<RoleChooseScreenProps> = ({ navigation }) => {
  const insets = useSafeAreaInsets();

  return (
    <View style={styles.screenContainer}>
      <View style={styles.backgroundContainer}>
        <GridBackground style={styles.singleGrid} height={1000} />
      </View>
      <View
        style={[
          styles.contentContainer,
          {
            paddingTop: insets.top,
            paddingBottom: insets.bottom,
          },
        ]}
      >
        <Image
          source={require('../assets/alsitoquezoncoloredlogo.png')}
          style={styles.logo}
        />
        <Text style={styles.subtitle}>Emergency Response App</Text>

        <TouchableOpacity
          style={[styles.button, styles.userButton]}
          onPress={() => navigation.navigate('UserHome')}
        >
          <Text style={styles.userText}>User login</Text>
        </TouchableOpacity>

        <Text style={styles.orText}>or</Text>

        <TouchableOpacity
          style={styles.responderButton}
          onPress={() => navigation.navigate('AdminHome')}
        >
          <Text style={styles.responderText}>Responder login</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  screenContainer: {
    flex: 1,
    backgroundColor: '#fff',
  },
  backgroundContainer: {
    position: 'absolute',
    width: '100%',
    height: '80%',
    left: 0,
    top: 0,
  },
  singleGrid: {
    height: '100%',
    top: 0,
  },
  contentContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: 20,
    transform: [{ translateY: -20 }],
  },
  logo: {
    width: 200,
    height: 200,
    resizeMode: 'contain',
    marginBottom: -30,
  },
  subtitle: {
    fontSize: 18,
    fontWeight: '500',
    color: '#000',
    marginTop: 0,
    marginBottom: 160,
    fontFamily: 'Montserrat_500Medium',
  },
  button: {
    width: '100%',
    maxWidth: 320,
    height: 60,
    justifyContent: 'center',
    alignItems: 'center',
    borderRadius: 10,
  },
  userButton: {
    backgroundColor: '#3B82F6',
  },
  userText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '500',
    fontFamily: 'Inter_500Medium',
  },
  orText: {
    marginVertical: 15,
    fontSize: 16,
    color: '#000',
    fontWeight: '500',
    fontFamily: 'Inter_500Medium',
  },
  responderButton: {
    padding: 10,
  },
  responderText: {
    color: '#000',
    fontSize: 18,
    fontWeight: '500',
    textDecorationLine: 'underline',
    fontFamily: 'Inter_500Medium',
  },
});

export default RoleChooseScreen;