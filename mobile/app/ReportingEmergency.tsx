import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  Dimensions,
  Image,
  TouchableOpacity,
} from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { useRouter, useLocalSearchParams } from 'expo-router';
import GridBackground from '../components/GridBackground';
import TopNavBar from '../components/TopNavBar';

const { width, height } = Dimensions.get('window');

const RED_COLOR = '#E63C3C';
const SHADE_COLOR = '#F9BEBE';
const HIGHLIGHT_COLOR = '#F3D8D8';
const BUTTON_BASE_SIZE = width * 0.35;

const CIRCLE_MAIN_SIZE = BUTTON_BASE_SIZE * 0.72;
const CIRCLE_MEDIUM_SIZE = BUTTON_BASE_SIZE * 0.864;
const CIRCLE_LARGE_SIZE = BUTTON_BASE_SIZE * 1.0368;

const RED_BOX_HEIGHT = height * 0.42;
const LOCATION_ICON_SIZE = 65;
const VERIFY_ICON_SIZE = 130;
const DROP_OFFSET = 5;

interface StatusProps {
  titlePrefix: string;
  titleHighlight: string;
  address: string;
}

const EmergencyStatusDisplay: React.FC<StatusProps> = ({
  titlePrefix,
  titleHighlight,
  address,
}) => {
  return (
    <View style={styles.redBoxContainer}>
      <View style={styles.redBoxContent}>
        <View style={styles.displayContainer}>
          <View style={styles.dropLayer} />
          <View style={styles.textBackground}>
            <View style={styles.titleRow}>
              <Text style={styles.titlePrefixText}>{titlePrefix}</Text>
              <View style={styles.titleHighlightContainer}>
                <Text style={styles.titleHighlightText}>{titleHighlight}</Text>
              </View>
            </View>
            <Text style={styles.redBoxAddress}>{address}</Text>
          </View>
        </View>
      </View>
    </View>
  );
};

const WavingEmergencyButton = () => (
  <View style={styles.buttonWrapper}>
    <View
      style={[
        styles.shadowCircle,
        {
          width: CIRCLE_LARGE_SIZE,
          height: CIRCLE_LARGE_SIZE,
          borderRadius: CIRCLE_LARGE_SIZE / 2,
          backgroundColor: HIGHLIGHT_COLOR,
        },
      ]}
    />
    <View
      style={[
        styles.shadowCircle,
        {
          width: CIRCLE_MEDIUM_SIZE,
          height: CIRCLE_MEDIUM_SIZE,
          borderRadius: CIRCLE_MEDIUM_SIZE / 2,
          backgroundColor: SHADE_COLOR,
        },
      ]}
    />
    <View
      style={[
        styles.circleMain,
        {
          width: CIRCLE_MAIN_SIZE,
          height: CIRCLE_MAIN_SIZE,
          borderRadius: CIRCLE_MAIN_SIZE / 2,
        },
      ]}
    >
      <Image
        source={require('../assets/locationicon2.png')}
        style={styles.locationIcon}
      />
    </View>
  </View>
);

export default function ReportingEmergency() {
  const insets = useSafeAreaInsets();
  const backgroundHeight = height * 2;
  const router = useRouter();
  const params = useLocalSearchParams();
  const [tapCount, setTapCount] = useState(0);

  const emergencyData = JSON.parse(params.emergencyData as string);
  const location = params.location as string;

  const statusTitlePrefix = 'Reporting';
  const statusTitleHighlight = `${emergencyData.label} Emergency`;
  const statusAddress = location || 'Current Location';

  useEffect(() => {
    if (tapCount === 5) {
      router.push({
        pathname: '/ReportVerified',
        params: {
          emergencyData: JSON.stringify(emergencyData),
          location: location,
        },
      });
      setTapCount(0);
    }
  }, [tapCount, router, emergencyData, location]);

  const handleScreenTap = () => {
    setTapCount(prevCount => prevCount + 1);
  };

  return (
    <TouchableOpacity
      activeOpacity={1}
      style={styles.container}
      onPress={handleScreenTap}
    >
      <TopNavBar
        title="Sending Location To Responders"
        theme="dark"
        isTransparent={true}
      />
      <GridBackground style={styles.singleGrid} height={backgroundHeight} />
      <View
        style={[styles.contentContainer, { paddingBottom: insets.bottom }]}
        pointerEvents="none"
      >
        <EmergencyStatusDisplay
          titlePrefix={statusTitlePrefix}
          titleHighlight={statusTitleHighlight}
          address={statusAddress}
        />
        <WavingEmergencyButton />
        <View style={styles.crowdsourceContainer}>
          <Text style={styles.crowdsourceText}>
            Verify the emergency {'\n'}report thru crowdsourcing
          </Text>
          <Image
            source={require('../assets/verifyreport.png')}
            style={styles.verifyIcon}
          />
        </View>
        <View style={styles.fillerSpace} />
      </View>
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  singleGrid: {
    position: 'absolute',
    top: 0,
    left: 0,
    zIndex: 1,
  },
  contentContainer: {
    flex: 1,
    zIndex: 2,
    paddingHorizontal: 0,
  },
  crowdsourceContainer: {
    alignItems: 'center',
    padding: 20,
    marginTop: BUTTON_BASE_SIZE * 0.5 + 20,
    zIndex: 2,
  },
  crowdsourceText: {
    fontFamily: 'Poppins-Medium',
    fontSize: 18,
    color: '#444',
    textAlign: 'center',
  },
  verifyIcon: {
    width: VERIFY_ICON_SIZE,
    height: VERIFY_ICON_SIZE,
    marginTop: 15,
  },
  fillerSpace: {
    flex: 1,
  },
  buttonWrapper: {
    justifyContent: 'center',
    alignItems: 'center',
    alignSelf: 'center',
    marginTop: -(BUTTON_BASE_SIZE * 0.5),
    zIndex: 30,
  },
  circleMain: {
    backgroundColor: RED_COLOR,
    justifyContent: 'center',
    alignItems: 'center',
    elevation: 8,
    zIndex: 3,
  },
  shadowCircle: {
    position: 'absolute',
    zIndex: 1,
    opacity: 1,
  },
  locationIcon: {
    width: LOCATION_ICON_SIZE,
    height: LOCATION_ICON_SIZE,
    resizeMode: 'contain',
    tintColor: '#fff',
  },
  redBoxContainer: {
    height: RED_BOX_HEIGHT,
    backgroundColor: RED_COLOR,
    borderBottomLeftRadius: 40,
    borderBottomRightRadius: 40,
    justifyContent: 'center',
    alignItems: 'center',
    zIndex: 10,
    width: '100%',
  },
  redBoxContent: {
    alignItems: 'center',
    paddingHorizontal: 20,
    width: '100%',
  },
  displayContainer: {
    width: '100%',
    paddingBottom: DROP_OFFSET,
  },
  dropLayer: {
    position: 'absolute',
    top: DROP_OFFSET,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: 'rgba(0, 0, 0, 0.3)',
    borderRadius: 15,
  },
  textBackground: {
    backgroundColor: '#F08A8A',
    padding: 20,
    borderRadius: 15,
    width: '100%',
    alignItems: 'center',
  },
  titleRow: {
    alignItems: 'center',
    justifyContent: 'center',
    flexDirection: 'row',
    marginBottom: 12,
  },
  titlePrefixText: {
    fontFamily: 'Poppins-Medium',
    fontSize: 18,
    color: '#000',
    textAlign: 'center',
  },
  titleHighlightContainer: {
    backgroundColor: 'rgba(25, 25, 25, 0.2)',
    borderRadius: 10,
    paddingHorizontal: 10,
    marginLeft: 8,
  },
  titleHighlightText: {
    fontFamily: 'Poppins-Medium',
    fontSize: 18,
    color: '#fff',
    textAlign: 'center',
  },
  redBoxAddress: {
    fontFamily: 'Poppins-Medium',
    fontSize: 14,
    color: '#000',
    marginTop: 8,
    textAlign: 'center',
  },
});