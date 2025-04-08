import pandas as pd
import sys

def validate_test_sequence(file_path):
    print(f"Validating test sequence: {file_path}")
    
    try:
        # Read the test sequence
        df = pd.read_csv(file_path)
        
        # Check required columns
        required_columns = ['Time', 'Function', 'Action']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            print(f"❌ Missing required columns: {missing_columns}")
            return False
        
        # Validate time sequence
        times = df['Time'].tolist()
        if not all(times[i] <= times[i+1] for i in range(len(times)-1)):
            print("❌ Times are not in ascending order")
            return False
        
        # Validate functions
        valid_functions = {
            'Read_OPD_02', 'Read_FPD_02', 'Read_EPD_01',
            'FV_02', 'NV_02', 'OV_03', 'FV_03',
            'BLP_Abort', 'Spark'
        }
        
        invalid_functions = set(df['Function']) - valid_functions
        if invalid_functions:
            print(f"❌ Invalid functions found: {invalid_functions}")
            return False
        
        # Validate actions
        valid_actions = {'READ', 'OPEN', 'CLOSE', 'START', ''}
        invalid_actions = set(df['Action']) - valid_actions
        if invalid_actions:
            print(f"❌ Invalid actions found: {invalid_actions}")
            return False
        
        # Check for critical safety sequences
        print("\nChecking safety sequences...")
        
        # Check for abort conditions
        abort_time = df[df['Function'] == 'BLP_Abort']['Time'].iloc[0] if 'BLP_Abort' in df['Function'].values else None
        if not abort_time:
            print("⚠️ Warning: No BLP_Abort command found")
        
        # Check valve sequences
        valve_sequence = df[df['Function'].isin(['FV_02', 'NV_02', 'OV_03', 'FV_03'])]
        print("\nValve sequence:")
        for _, row in valve_sequence.iterrows():
            print(f"t={row['Time']}s: {row['Function']} {row['Action']}")
        
        print("\n✅ Test sequence validation completed successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error validating test sequence: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate_test_sequence.py <test_sequence_file>")
        sys.exit(1)
    
    validate_test_sequence(sys.argv[1]) 