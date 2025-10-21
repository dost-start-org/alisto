import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  Image,
  TextInput,
  TouchableOpacity,
  Dimensions,
} from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { useRoute, RouteProp } from '@react-navigation/native';

const { height, width } = Dimensions.get('window');

const HEADER_HEIGHT = height * 0.15;
const CARD_MARGIN_HORIZONTAL = 20;
const CARD_PADDING = 20;
const BORDER_RADIUS_LARGE = 30;
const BORDER_RADIUS_SMALL = 10;

const COLOR_VERIFIED_GREEN = '#0FB300';
const COLOR_CARD_MAIN = '#E83737';
const COLOR_CARD_MID = '#F9BEBE';
const COLOR_CARD_BACK = '#F3D8D3';
const COLOR_BUTTON_SUBMIT = '#2773FF';
const COLOR_BUTTON_ARRIVED = '#4CAF50';
const DARK_GRAY = '#3A3A3A';
const MEDIUM_GRAY = '#9c9b9bff';
const LIGHT_GRAY_BACKGROUND = '#F7F7F7';
const LIGHT_PINK_BACKGROUND = '#FEF2F2';

const WAVE_OFFSET_V_MIDDLE = 20;
const WAVE_OFFSET_V_BACK = 40;

const MIDDLE_CARD_WIDER_PERCENT = 0.03;
const MIDDLE_CARD_EXTENSION = (width * MIDDLE_CARD_WIDER_PERCENT) / 2;

const BACK_CARD_WIDER_PERCENT = 0.05;
const BACK_CARD_EXTENSION = (width * BACK_CARD_WIDER_PERCENT) / 2;

type RootStackParamList = {
  ReportVerifiedScreen: {
    emergencyData: { label: string; title: string; icon: any };
    location: string;
  };
};

type ReportVerifiedScreenRouteProp = RouteProp<
  RootStackParamList,
  'ReportVerifiedScreen'
>;

export default function ReportVerifiedScreen() {
  const [incidentDetails, setIncidentDetails] = useState('');
  const insets = useSafeAreaInsets();

  const route = useRoute<ReportVerifiedScreenRouteProp>();
  const { emergencyData } = route.params;

  const emergencyLabel = emergencyData.label;
  const statusTitleText = `${emergencyLabel} responders is on their way`;

  const bureauName = `Bureau of ${emergencyLabel} Marikina City`;

  const bureauIconSource = emergencyData.icon;

  return (
    <View style={[styles.safeAreaContainer, { paddingTop: insets.top }]}>
      <View style={[styles.header, { height: HEADER_HEIGHT }]}>
        <Text style={styles.verifiedText}>Your report has been verified</Text>
        <Image
          source={require('../assets/reportverified.png')}
          style={styles.checkmarkIcon}
        />
      </View>

      <View style={styles.contentContainer}>
        <View style={styles.statusCardContainer}>
          <View style={styles.waveBack} />
          <View style={styles.waveMid} />

          <View style={styles.statusCard}>
            <View style={styles.statusLabelPill}>
              <Text style={styles.statusLabel}>REPORT STATUS</Text>
            </View>

            <Text style={styles.statusTitle}>{statusTitleText}</Text>

            <View style={styles.etaContainer}>
              <Text style={styles.etaText}>To arrive in</Text>
              <View style={styles.etaBubble}>
                <Text style={styles.etaBubbleText}>&lt; 5 minutes</Text>
              </View>
            </View>

            <View style={styles.bureauCard}>
              <View>
                <Text style={styles.bureauText}>{bureauName}</Text>

                <Text style={styles.bureauPhone}>09123456789</Text>
              </View>
              <Image
                source={bureauIconSource}
                style={styles.bureauIcon}
              />
            </View>
          </View>
        </View>

        <View style={styles.formContainer}>
          <Text style={styles.infoPrompt}>
            Give more information about the incident?
          </Text>
          <TextInput
            style={styles.textInput}
            placeholder="What happened?"
            placeholderTextColor={MEDIUM_GRAY}
            multiline
            value={incidentDetails}
            onChangeText={setIncidentDetails}
          />

          <TouchableOpacity style={styles.submitButton}>
            <Image
              source={require('../assets/submiticon.png')}
              style={styles.sendIcon}
            />
            <Text style={styles.submitButtonText}>Submit</Text>
          </TouchableOpacity>
        </View>
      </View>

      <View style={[styles.bottomSheetBackground, { paddingBottom: insets.bottom }]}>
        <View style={styles.arrivedButtonContainer}>
          <TouchableOpacity style={styles.arrivedButton}>
            <Text style={styles.arrivedButtonText}>The responders has arrived</Text>
          </TouchableOpacity>
        </View>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  safeAreaContainer: {
    flex: 1,
    backgroundColor: LIGHT_PINK_BACKGROUND,
  },
  header: {
    backgroundColor: LIGHT_PINK_BACKGROUND,
    justifyContent: 'center',
    alignItems: 'center',
    flexDirection: 'row',
    paddingHorizontal: 20,
  },
  verifiedText: {
    fontSize: 20,
    fontFamily: 'Poppins-Medium',
    color: COLOR_VERIFIED_GREEN,
    marginRight: 10,
  },
  checkmarkIcon: {
    width: 40,
    height: 40,
    resizeMode: 'contain',
  },
  contentContainer: {
    flex: 1,
    backgroundColor: LIGHT_GRAY_BACKGROUND,
    paddingTop: CARD_PADDING,
  },
  formContainer: {
    paddingHorizontal: CARD_MARGIN_HORIZONTAL,
    width: 350,
    flex: 1,
    alignSelf: 'center',
  },
  statusCardContainer: {
    marginBottom: 60,
    position: 'relative',
  },
  waveBack: {
    position: 'absolute',
    backgroundColor: COLOR_CARD_BACK,
    borderRadius: BORDER_RADIUS_LARGE,
    top: -WAVE_OFFSET_V_BACK,
    bottom: -WAVE_OFFSET_V_BACK,
    left: -BACK_CARD_EXTENSION,
    right: -BACK_CARD_EXTENSION,
    zIndex: 1,
  },
  waveMid: {
    position: 'absolute',
    backgroundColor: COLOR_CARD_MID,
    borderRadius: BORDER_RADIUS_LARGE,
    top: -WAVE_OFFSET_V_MIDDLE,
    bottom: -WAVE_OFFSET_V_MIDDLE,
    left: -MIDDLE_CARD_EXTENSION,
    right: -MIDDLE_CARD_EXTENSION,
    zIndex: 2,
  },
  statusCard: {
    backgroundColor: COLOR_CARD_MAIN,
    borderRadius: BORDER_RADIUS_LARGE,
    paddingVertical: CARD_PADDING,
    alignItems: 'flex-start',
    zIndex: 3,
    paddingBottom: 100,
    marginHorizontal: 0,
    paddingHorizontal: CARD_PADDING,
  },
  statusLabelPill: {
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
    borderRadius: 20,
    paddingHorizontal: 10,
    paddingVertical: 4,
    marginBottom: 10,
    overflow: 'hidden',
  },
  statusLabel: {
    fontSize: 14,
    fontFamily: 'Poppins-Medium',
    color: '#FFFFFF',
  },
  statusTitle: {
    fontSize: 20,
    fontFamily: 'Poppins-Medium',
    color: '#FFFFFF',
    marginBottom: 10,
  },
  etaContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: 5,
  },
  etaText: {
    fontSize: 12,
    color: 'rgba(255,255,255,0.8)',
    marginRight: 10,
    fontFamily: 'Poppins-Medium',
  },
  etaBubble: {
    backgroundColor: 'rgba(0, 0, 0, 0.2)',
    borderRadius: 20,
    paddingHorizontal: 10,
    paddingVertical: 2,
  },
  etaBubbleText: {
    fontSize: 14,
    fontFamily: 'Poppins-Medium',
    color: '#FFFFFF',
  },
  bureauCard: {
    backgroundColor: '#FFFFFF',
    borderRadius: BORDER_RADIUS_SMALL,
    paddingVertical: 8,
    paddingHorizontal: 12,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    position: 'absolute',
    bottom: CARD_PADDING,
    left: CARD_PADDING,
    right: undefined,
    alignSelf: 'flex-start',
    zIndex: 10,
    elevation: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.15,
    shadowRadius: 10,
  },
  bureauText: {
    fontSize: 14,
    fontFamily: 'Poppins-Medium',
    color: DARK_GRAY,
    lineHeight: 20,
    marginRight: 10,
  },
  bureauPhone: {
    fontSize: 14,
    color: MEDIUM_GRAY,
    fontFamily: 'Poppins-Medium',
  },
  bureauIcon: {
    width: 35,
    height: 35,
    resizeMode: 'contain',
  },
  infoPrompt: {
    fontSize: 15,
    fontFamily: 'Poppins-Medium',
    color: DARK_GRAY,
    marginTop: 40,
    marginBottom: 4,
  },
  textInput: {
    height: 115,
    backgroundColor: '#FFFFFF',
    borderRadius: BORDER_RADIUS_SMALL,
    padding: 15,
    textAlignVertical: 'top',
    fontSize: 16,
    color: DARK_GRAY,
    marginBottom: 15,
    borderWidth: 1,
    borderColor: '#E0E0E0',
    fontFamily: 'Poppins-Medium',
  },
  submitButton: {
    backgroundColor: COLOR_BUTTON_SUBMIT,
    flexDirection: 'row',
    alignSelf: 'flex-end',
    alignItems: 'center',
    paddingVertical: 4,
    paddingHorizontal: 8,
    borderRadius: BORDER_RADIUS_SMALL,
    marginBottom: 20,
  },
  sendIcon: {
    width: 16,
    height: 16,
    resizeMode: 'contain',
    marginRight: 8,
  },
  submitButtonText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontFamily: 'Poppins-Medium',
  },
  arrivedButtonContainer: {
    paddingHorizontal: CARD_MARGIN_HORIZONTAL,
    paddingTop: 20,
    paddingBottom: 20,
    width: '100%',
  },
  arrivedButton: {
    backgroundColor: COLOR_BUTTON_ARRIVED,
    paddingVertical: 18,
    borderRadius: BORDER_RADIUS_LARGE,
    alignItems: 'center',
    justifyContent: 'center',
  },
  arrivedButtonText: {
    color: '#FFFFFF',
    fontSize: 18,
    fontFamily: 'Poppins-Medium',
  },
  bottomSheetBackground: {
    position: 'absolute',
    bottom: 0,
    left: 0,
    right: 0,
    height: height * 0.15,
    backgroundColor: '#FFFFFF',
    borderTopLeftRadius: BORDER_RADIUS_LARGE,
    borderTopRightRadius: BORDER_RADIUS_LARGE,
    zIndex: 4,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: -5 },
    shadowOpacity: 0.1,
    shadowRadius: 10,
    elevation: 10,
    alignItems: 'center',
    justifyContent: 'flex-start',
  },
});