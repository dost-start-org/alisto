import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Image,
  ScrollView,
  Linking,
  Platform,
} from 'react-native';
import { useRouter } from 'expo-router';
import BottomNav from '../components/BottomNav';
import TopNav from '../components/TopNavUserHome';
import GridBackground from '../components/GridBackground';

type HotlineOption =
  | 'Fire'
  | 'Medical Emergency'
  | 'Police'
  | 'Disaster Rescue';

export default function Hotlines() {
  const router = useRouter();
  const [selectedHotline, setSelectedHotline] = useState<HotlineOption | null>(
    null
  );

  const options: { label: HotlineOption; icon: any }[] = [
    { label: 'Fire', icon: require('../assets/fireemergencyicon.png') },
    {
      label: 'Medical Emergency',
      icon: require('../assets/hospitalemergencyicon.png'),
    },
    { label: 'Police', icon: require('../assets/policeemergencyicon.png') },
    {
      label: 'Disaster Rescue',
      icon: require('../assets/disasterresponseemergencyicon.png'),
    },
  ];

  const userContacts = Array.from({ length: 20 }).map((_, i) => ({
    id: `user-${i}`,
    name: 'Maria Clara',
    role: 'Mother',
    phone: '09171234567',
  }));

  const hotlineData: Record<HotlineOption, any[]> = {
    Fire: Array.from({ length: 5 }).map((_, i) => ({
      id: `fire-${i}`,
      name: 'Fire Station ' + (i + 1),
      role: 'Bureau of Fire Protection',
      phone: '9876543210',
    })),
    'Medical Emergency': Array.from({ length: 5 }).map((_, i) => ({
      id: `med-${i}`,
      name: 'General Hospital ' + (i + 1),
      role: 'Emergency Room',
      phone: '09123456789',
    })),
    Police: Array.from({ length: 5 }).map((_, i) => ({
      id: `police-${i}`,
      name: 'Police Precinct ' + (i + 1),
      role: 'Philippine National Police',
      phone: '117',
    })),
    'Disaster Rescue': Array.from({ length: 5 }).map((_, i) => ({
      id: `disaster-${i}`,
      name: 'Rescue Unit ' + (i + 1),
      role: 'NDRRMC',
      phone: '911',
    })),
  };

  const handleCall = (phoneNumber: string) => {
    let phoneUrl = '';
    if (Platform.OS === 'android') {
      phoneUrl = `tel:${phoneNumber}`;
    } else {
      phoneUrl = `telprompt:${phoneNumber}`;
    }
    Linking.canOpenURL(phoneUrl)
      .then((supported) => {
        if (supported) {
          return Linking.openURL(phoneUrl);
        }
      })
      .catch((err) => console.error('An error occurred', err));
  };

  const renderContactList = (contacts: any[]) => {
    return contacts.map((item) => (
      <View key={item.id} style={styles.contactCard}>
        <Image
          source={require('../assets/contactspersonicon.png')}
          style={styles.contactIcon}
        />
        <View style={styles.contactInfo}>
          <Text style={styles.contactName}>{item.name}</Text>
          <Text style={styles.contactRole}>{item.role}</Text>
        </View>
        <TouchableOpacity onPress={() => handleCall(item.phone)}>
          <Image
            source={require('../assets/contactscallicon.png')}
            style={styles.contactRightIcon}
          />
        </TouchableOpacity>
      </View>
    ));
  };

  const renderHotlineView = () => (
    <>
      <View style={styles.hotlineHeader}>
        <TouchableOpacity
          onPress={() => setSelectedHotline(null)}
          style={styles.backButton}
        >
          <Image
            source={require('../assets/backicon.png')}
            style={styles.backIcon}
          />
        </TouchableOpacity>
        <Text style={styles.hotlineTitle}>{selectedHotline}</Text>
      </View>
      {renderContactList(hotlineData[selectedHotline!])}
    </>
  );

  const renderDefaultView = () => (
    <>
      <Text style={styles.titleText}>HOTLINES</Text>
      <View style={styles.pillsWrapper}>
        {options.map((opt) => (
          <TouchableOpacity
            key={opt.label}
            style={styles.pill}
            onPress={() => setSelectedHotline(opt.label)}
          >
            <Text style={styles.pillText}>{opt.label.replace('\\n', ' ')}</Text>
            {opt.icon && <Image source={opt.icon} style={styles.pillIcon} />}
          </TouchableOpacity>
        ))}
      </View>

      <View style={styles.headerRow}>
        <Text style={styles.headerText}>Your Emergency Contacts</Text>
        <TouchableOpacity style={styles.addButton}>
          <Image
            source={require('../assets/addcontactsicon.png')}
            style={styles.addIcon}
          />
          <Text style={styles.addText}>Add</Text>
        </TouchableOpacity>
      </View>
      {renderContactList(userContacts)}
    </>
  );

  return (
    <View style={styles.container}>
      <TopNav />
      <View style={styles.backgroundContainer}>
        <GridBackground style={styles.singleGrid} height={2000} />
      </View>

      <ScrollView
        style={styles.scrollArea}
        contentContainerStyle={{ paddingBottom: 80 }}
      >
        {selectedHotline ? renderHotlineView() : renderDefaultView()}
      </ScrollView>

      <BottomNav
        onNavigate={(screen) => {
          router.push(`/${screen}`);
        }}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#e5e5e5' },
  backgroundContainer: {
    position: 'absolute',
    marginTop: 70,
    width: '100%',
    height: '90%',
    left: 0,
    top: 0,
    zIndex: -1,
  },
  singleGrid: { height: '100%', top: 0 },
  scrollArea: { flex: 1, paddingVertical: 16, paddingHorizontal: 24 },
  titleText: {
    fontSize: 25,
    color: '#595959',
    fontFamily: 'Inter',
    fontWeight: 'bold',
    alignSelf: 'flex-start',
    marginTop: 10,
  },
  pillsWrapper: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
    marginVertical: 20,
  },
  pill: {
    width: '48%',
    backgroundColor: '#f2f2f2',
    paddingHorizontal: 10,
    paddingVertical: 2,
    borderRadius: 10,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginBottom: 12,
    elevation: 2,
    minHeight: 70,
  },
  pillIcon: { width: 43, height: 43, resizeMode: 'contain' },
  pillText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#000',
    fontFamily: 'Inter',
    flex: 1,
  },
  headerRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginTop: 12,
    marginBottom: 24,
  },
  headerText: {
    fontSize: 20,
    fontWeight: '700',
    color: '#000',
    fontFamily: 'Inter',
  },
  addButton: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#3A3A3A',
    paddingLeft: 2,
    paddingRight: 14,
    paddingVertical: 0,
    borderRadius: 6,
  },
  addIcon: { width: 48, height: 48, marginRight: 6, resizeMode: 'contain' },
  addText: {
    color: '#fff',
    fontSize: 14,
    fontWeight: '600',
    fontFamily: 'Inter',
  },
  contactCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#fafafa',
    padding: 12,
    borderRadius: 8,
    marginBottom: 10,
  },
  contactIcon: { width: 34, height: 34, marginRight: 10, resizeMode: 'contain' },
  contactInfo: { flex: 1, justifyContent: 'center' },
  contactName: {
    fontSize: 18,
    fontWeight: '600',
    color: '#000',
    fontFamily: 'Inter',
  },
  contactRole: { fontSize: 14, color: '#666', fontFamily: 'Inter' },
  contactRightIcon: { width: 24, height: 24, resizeMode: 'contain' },
  hotlineHeader: {
    marginBottom: 20,
    flexDirection: 'row',
    alignItems: 'center',
  },
  hotlineTitle: {
    fontSize: 26,
    fontWeight: 'bold',
    color: '#333',
    fontFamily: 'Inter',
    marginLeft: 10,
  },
  backButton: {},
  backIcon: {
    width: 30,
    height: 30,
    resizeMode: 'contain',
  },
});

