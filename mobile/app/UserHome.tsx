import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  Pressable,
  ActivityIndicator,
} from 'react-native';
import { useRouter } from 'expo-router';
import EmergencyButton from '../components/EmergencyButton';
import BottomNav from '../components/BottomNav';
import TopNav from '../components/TopNavUserHome';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import GridBackground from '../components/GridBackground';
import CrowdsourceUserScreen from '../components/CrowdsourceUserScreen';
import * as SecureStore from 'expo-secure-store';
import AsyncStorage from '@react-native-async-storage/async-storage';

type UserProfile = {
  id: string;
  full_name: string;
  authority_level: string;
  contact_number: string;
  address: string;
  status: string;
};

export default function UserHome() {
  const insets = useSafeAreaInsets();
  const router = useRouter();
  const [clickCount, setClickCount] = useState(0);
  const [isModalVisible, setIsModalVisible] = useState(false);

  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const crowdsourceData = {
    id: 'report-12345',
    emergencyType: 'fire',
    location: '023, Socorro St. Brgy. Discaya, Quezon City',
    timestamp: '2025-10-20T02:46:00.000Z',
  };

  useEffect(() => {
    const loadData = async () => {
      try {
        const savedToken = await SecureStore.getItemAsync('authToken');
        const savedProfileString = await AsyncStorage.getItem('userProfile');

        if (savedToken && savedProfileString) {
          const loadedProfile = JSON.parse(savedProfileString);
          console.log('--- USER PROFILE LOADED ---:', loadedProfile);
          setProfile(loadedProfile);
        } else {
          router.replace('/');
        }
      } catch (e) {
        console.error('Failed to load data, redirecting to login.', e);
        router.replace('/');
      } finally {
        setIsLoading(false);
      }
    };

    loadData();
  }, [router, setProfile]);

  const handleSecretClick = () => {
    const newClickCount = clickCount + 1;

    if (newClickCount === 5) {
      console.log('--- 5-CLICK PROFILE LOG ---:', profile);
      setClickCount(newClickCount);
    } else if (newClickCount >= 10) {
      setIsModalVisible(true);
      setClickCount(0);
    } else {
      setClickCount(newClickCount);
    }
  };

  if (isLoading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" />
        <Text>Loading...</Text>
      </View>
    );
  }

  return (
    <>
      <Pressable style={styles.container} onPress={handleSecretClick}>
        <TopNav />

        <View style={styles.backgroundContainer}>
          <GridBackground style={styles.singleGrid} height={2000} />
        </View>
        <View
          style={[
            styles.contentContainer,
            {
              paddingTop: insets.top,
              paddingBottom: insets.bottom,
            },
          ]}
        />
        <View style={styles.middle}>
          <EmergencyButton />

          <View style={styles.announcementSection}>
            <Text style={styles.announcementTitle}>Announcements</Text>
            <View style={styles.announcementBox}>
              <Text style={styles.announcementText}> </Text>
            </View>
          </View>
        </View>

        <BottomNav
          onNavigate={(screen) => {
            router.push(`/${screen}`);
          }}
        />
      </Pressable>

      {isModalVisible && <View style={styles.dimOverlay} />}

      {isModalVisible && (
        <View style={styles.modalContainer}>
          <CrowdsourceUserScreen
            onClose={() => setIsModalVisible(false)}
            data={crowdsourceData}
          />
        </View>
      )}
    </>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#e5e5e5' },
  screenContainer: {
    flex: 1,
    backgroundColor: '#fff',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  backgroundContainer: {
    position: 'absolute',
    marginTop: 70,
    width: '100%',
    height: '90%',
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
    display: 'none',
    transform: [{ translateY: -20 }],
  },
  topNav: {
    height: 60,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 16,
    backgroundColor: '#f2f2f2',
    elevation: 2,
  },
  logoContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  logo: { width: 100, height: 35, resizeMode: 'contain' },
  cityText: {
    fontSize: 16,
    fontWeight: '600',
    marginLeft: 6,
    color: '#333',
  },
  hamburger: { fontSize: 22, fontWeight: 'bold' },
  middle: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: 16,
  },
  announcementSection: {
    width: '95%',
    marginTop: 60,
  },
  announcementTitle: {
    fontSize: 18,
    fontWeight: '600',
    fontFamily: 'Inter',
    color: '#333',
    marginBottom: 6,
  },
  announcementBox: {
    backgroundColor: '#d1d1d1',
    borderRadius: 8,
    padding: 16,
    minHeight: 180,
  },
  announcementText: {
    fontSize: 14,
    fontFamily: 'Inter',
    color: '#333',
    lineHeight: 20,
  },
  dimOverlay: {
    ...StyleSheet.absoluteFillObject,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    zIndex: 51,
  },
  modalContainer: {
    ...StyleSheet.absoluteFillObject,
    justifyContent: 'center',
    alignItems: 'center',
    zIndex: 52,
  },
});