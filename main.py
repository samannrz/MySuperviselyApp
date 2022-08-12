
# start using supervisely API
# This codes takes some statistics on the video projects
import supervisely as sly
import pandas as pd

# Saman's Token
mytoken = 'jXCVEbySH8moyTXLihkoE1k9UX4fTMDUYkHMJgUoIzx0EnyS5outN8de6UvUCjdGfRUr8D553l8MhTLQkzDOm22bKTsJulgDiGzy2Z4yYEmFmhcsL8k37Af837qXb2UO'

api = sly.Api(server_address="http://surgai-surgery.com", token=mytoken)

# let's test that authentication was successful and we can communicate with the platform
my_teams = api.team.get_list()
print(f"I'm a member of {len(my_teams)} teams")

# Define the team name
tm = api.team.get_info_by_name('Endometriosis')
ws = api.workspace.get_info_by_name(tm.id, 'Data annotation')
print('Here is %s team and %s workspace' % (tm.name, ws.name))
prs = api.project.get_list(ws.id)
prList = []
dsList = []
vdList = []
nframesList = []
nAnnframesList = []

for pr in prs:
    dss = api.dataset.get_list(pr.id)
    print('%d datasets in %s project' % (len(dss), pr.name))
    for ds in dss:  # going  through datasets to collect their statistics
        vds = api.video.get_list(ds.id)
        nframes = 0
        nAnnframes = 0
        for vd in vds:
            # print('%d : Total number of frames for %s'%(len(vd.frames_to_timecodes),vd.name))
            ans = api.video.annotation.download(vd.id)
            nframes = ans['framesCount'] + nframes  # count Total number of frames in the dataset
            nAnnframes = nAnnframes + len(ans['frames'])  # count n of annotatedframes in the dataset
        prList.append(pr.name)
        dsList.append(ds.name)
        vdList.append(len(vds))
        nframesList.append(nframes)
        nAnnframesList.append(nAnnframes)

# Create the dataframe
prCol = 'Project'
dsCol = 'Dataset'
vdCol = 'n. videos'
nfCol = 'n. Frames'
nAnnCol = 'n. Annotated Frames'
prList.append('Total')
dsList.append('')
vdList.append(sum(vdList))
nframesList.append(sum(nframesList))
nAnnframesList.append(sum(nAnnframesList))

data_df = pd.DataFrame({prCol: prList, dsCol: dsList, vdCol: vdList, nfCol: nframesList, nAnnCol: nAnnframesList})
print(data_df)

# save the dataframe to csv
job_info = api.labeling_job.get_info_by_id(job_id)
if job_info is None:
    raise RuntimeError('Labeling job id={!r} not found'.format(job_id))
dest_dir = os.path.join(sly.TaskPaths.OUT_ARTIFACTS_DIR, "job_id_{}_name_{}".format(job_info.id, job_info.name))
sly.fs.mkdir(dest_dir)

data_df.to_csv(os.path.join(dest_dir, 'activity.csv'))