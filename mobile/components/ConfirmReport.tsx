import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Dimensions,
  Image,
  TouchableWithoutFeedback,
  BackHandler,
} from 'react-native';

const { width, height } = Dimensions.get('window');

type ConfirmReportProps = {
  visible: boolean;
  onConfirm: () => void;
  onCancel: () => void;
};

export default function ConfirmReport({ visible, onConfirm, onCancel }: ConfirmReportProps) {
  React.useEffect(() => {
    const backHandler = BackHandler.addEventListener('hardwareBackPress', () => {
      if (visible) {
        onCancel();
        return true;
      }
      return false;
    });
    return () => backHandler.remove();
  }, [visible, onCancel]);

  if (!visible) return null;

  return (
    <TouchableWithoutFeedback onPress={onCancel}>
      <View style={styles.modalBackground}>
        <TouchableWithoutFeedback>
          <View style={styles.modalContainer}>
            <Image
              source={require('../assets/warningicon.png')}
              style={styles.warningIcon}
            />
            <Text style={styles.modalTitle}>Are you sure about this report?</Text>
            <Text style={styles.modalSubtitle}>
              Prank incident report has serious consequences
            </Text>
            <View style={{ height: height * 0.05 }} />
            <TouchableOpacity style={styles.confirmButton} onPress={onConfirm}>
              <Text style={styles.confirmButtonText}>Confirm</Text>
            </TouchableOpacity>
          </View>
        </TouchableWithoutFeedback>
      </View>
    </TouchableWithoutFeedback>
  );
}

const styles = StyleSheet.create({
  modalBackground: {
    position: 'absolute',
    top: 0,
    left: 0,
    width,
    height,
    backgroundColor: 'rgba(0,0,0,0.5)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  modalContainer: {
    width: width * 0.85,
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 20,
    alignItems: 'center',
  },
  warningIcon: {
    width: width * 0.2,
    height: width * 0.2,
    resizeMode: 'contain',
    marginBottom: 20,
  },
  modalTitle: {
    fontSize: 18,
    fontWeight: '700',
    color: '#000',
    textAlign: 'center',
  },
  modalSubtitle: {
    fontSize: 14,
    fontWeight: '600',
    color: '#FFD700',
    textAlign: 'center',
    paddingTop: 8,
  },
  confirmButton: {
    backgroundColor: '#007AFF',
    paddingVertical: 14,
    paddingHorizontal: 40,
    borderRadius: 12,
    width: '70%',
    alignItems: 'center',
  },
  confirmButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '700',
  },
});
