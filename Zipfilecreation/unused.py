import boto3

def lambda_handler(event, context):

    region = "us-west-2"

    ec2 = boto3.client('ec2', region_name=region)
    rds = boto3.client('rds', region_name=region)

    unused_volumes = []
    unused_snapshots = []

    # ----------------------------
    # Find Unused EBS Volumes
    # ----------------------------
    volumes = ec2.describe_volumes()

    for vol in volumes['Volumes']:
        if vol['State'] == 'available':
            unused_volumes.append({
                "VolumeId": vol['VolumeId'],
                "Size": vol['Size'],
                "CreateTime": str(vol['CreateTime'])
            })

    # ----------------------------
    # Find Manual RDS Snapshots
    # ----------------------------
    snapshots = rds.describe_db_snapshots(SnapshotType='manual')

    for snap in snapshots['DBSnapshots']:
        unused_snapshots.append({
            "SnapshotId": snap['DBSnapshotIdentifier'],
            "DBInstance": snap['DBInstanceIdentifier'],
            "CreateTime": str(snap['SnapshotCreateTime'])
        })

    result = {
        "Unused_EBS_Volumes": unused_volumes,
        "Manual_RDS_Snapshots": unused_snapshots
    }

    print(result)

    return result